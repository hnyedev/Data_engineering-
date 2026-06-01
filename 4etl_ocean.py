"""
================================================================================
DAG: ocean_etl_demo
================================================================================
GOAL:
    Simple ETL demo pipeline — extracts daily ocean conditions from the
    Open-Meteo Marine API (free, no key needed), cleans the data, and
    produces basic aggregations saved as JSON.

STRUCTURE:
    extract_ocean ──► clean ──► aggregate ──► load

DATA SOURCE:
    https://marine-api.open-meteo.com/v1/marine
    Fields: wave_height, wave_period, wave_direction, ocean_current_speed

LOCATION:
    Gulf of Mexico — lat: 23.0, lon: -90.0

OUTPUT:
    /opt/airflow/data/ocean_summary_YYYYMMDD.json

AUTHOR : Cesar Pinto
LAB    : 4 - ETL Airflow Orchestration
================================================================================
"""

from airflow.decorators import dag, task
from datetime import datetime, timedelta
import requests
import pandas as pd
import json
from pathlib import Path


default_args = {
    "owner": "cesar_pinto",
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

LAT = 23.0
LON = -90.0


@dag(
    dag_id="ocean_etl_demo",
    description="Simple ocean conditions ETL — demo pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["etl", "demo", "ocean", "marine"],
)
def ocean_etl_demo():

    # -----------------------------------------------------------------------
    # TASK 1 — Extract
    # -----------------------------------------------------------------------
    @task()
    def extract_ocean(execution_date=None) -> dict:
        """
        Pulls hourly marine data from Open-Meteo Marine API.
        Returns raw hourly dict.
        """
        date_str = (execution_date - timedelta(days=1)).strftime("%Y-%m-%d")
        print(f"[extract] Fetching ocean data for {date_str}")

        resp = requests.get(
            "https://marine-api.open-meteo.com/v1/marine",
            params={
                "latitude":   LAT,
                "longitude":  LON,
                "hourly":     "wave_height,wave_period,wave_direction,ocean_current_speed",
                "start_date": date_str,
                "end_date":   date_str,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()["hourly"]
        print(f"[extract] Got {len(data['time'])} records")
        return data

    # -----------------------------------------------------------------------
    # TASK 2 — Clean
    # -----------------------------------------------------------------------
    @task()
    def clean(raw: dict) -> dict:
        """
        - Parses timestamps
        - Drops fully-null rows
        - Clamps wave height to physically plausible range (0-30m)
        """
        df = pd.DataFrame(raw)
        df.rename(columns={"time": "timestamp"}, inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        before = len(df)
        df.dropna(how="all", subset=["wave_height", "wave_period"], inplace=True)
        print(f"[clean] Dropped {before - len(df)} null rows")

        df["wave_height"] = df["wave_height"].clip(0, 30)
        df["ocean_current_speed"] = df["ocean_current_speed"].clip(0, 5)

        print(f"[clean] Clean rows: {len(df)}")
        return df.to_dict(orient="records")

    # -----------------------------------------------------------------------
    # TASK 3 — Aggregate
    # -----------------------------------------------------------------------
    @task()
    def aggregate(records: list, execution_date=None) -> dict:
        """
        Computes daily summary stats:
        - mean / max wave height
        - mean wave period
        - dominant wave direction (mode)
        - mean current speed
        - sea state label (Beaufort-style)
        """
        df = pd.DataFrame(records)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        def sea_state(h: float) -> str:
            if h < 0.1:  return "Calm"
            if h < 0.5:  return "Rippled"
            if h < 1.25: return "Slight"
            if h < 2.5:  return "Moderate"
            if h < 4.0:  return "Rough"
            return "Very rough"

        mean_height = df["wave_height"].mean()

        summary = {
            "date":               (execution_date - timedelta(days=1)).strftime("%Y-%m-%d"),
            "location":           {"lat": LAT, "lon": LON, "zone": "Gulf of Mexico"},
            "wave_height_m": {
                "mean": round(mean_height, 2),
                "max":  round(df["wave_height"].max(), 2),
                "min":  round(df["wave_height"].min(), 2),
            },
            "wave_period_s": {
                "mean": round(df["wave_period"].mean(), 2),
                "max":  round(df["wave_period"].max(), 2),
            },
            "dominant_direction_deg": round(df["wave_direction"].mode()[0], 1),
            "current_speed_ms": {
                "mean": round(df["ocean_current_speed"].mean(), 3),
                "max":  round(df["ocean_current_speed"].max(), 3),
            },
            "sea_state":  sea_state(mean_height),
            "total_hours": len(df),
        }

        print(f"[aggregate] Sea state: {summary['sea_state']}")
        print(f"[aggregate] Mean wave height: {summary['wave_height_m']['mean']} m")
        return summary

    # -----------------------------------------------------------------------
    # TASK 4 — Load
    # -----------------------------------------------------------------------
    @task()
    def load(summary: dict) -> str:
        """
        Saves the daily summary as a JSON file.
        """
        data_dir = Path("/opt/airflow/data")
        data_dir.mkdir(parents=True, exist_ok=True)

        date_tag = summary["date"].replace("-", "")
        out_path = data_dir / f"ocean_summary_{date_tag}.json"

        with open(out_path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"[load] Saved → {out_path}")
        return str(out_path)

    # -----------------------------------------------------------------------
    # WIRING
    # -----------------------------------------------------------------------
    raw     = extract_ocean()
    cleaned = clean(raw)
    summary = aggregate(cleaned)
    load(summary)


dag_instance = ocean_etl_demo()
