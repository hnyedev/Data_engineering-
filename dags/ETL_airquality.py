from airflow.decorators import dag, task
from datetime import datetime, timedelta
import requests
import pandas as pd
from pathlib import Path

# ---------------- CONFIG ----------------
LAT, LON = 20.97, -89.62  # Mérida
DATA_DIR = Path("/opt/airflow/data")
DATA_DIR.mkdir(exist_ok=True)

POLLUTANTS = {
    "pm2_5": "PM2.5",
    "pm10": "PM10",
    "ozone": "O3",
    "nitrogen_dioxide": "NO2",
    "carbon_monoxide": "CO",
    "european_aqi": "AQI",
}

default_args = {
    "owner": "cesar_pinto",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

# ---------------- DAG ----------------
@dag(
    dag_id="Daily_air_quality",
    default_args=default_args,
    start_date=datetime(2026, 3, 27),
    schedule_interval="@daily",
    catchup=False,
)
def etl_air_quality():

    # -------- EXTRACT AIR QUALITY --------
    @task()
    def extract_airquality():
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": LAT,
            "longitude": LON,
            "hourly": ",".join(POLLUTANTS.keys()),
        }
        res = requests.get(url, params=params)
        data = res.json()["hourly"]
        print("[extract_airquality] OK")
        return data

    # -------- EXTRACT WEATHER --------
    @task()
    def extract_weather():
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": LAT,
            "longitude": LON,
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m",
        }
        res = requests.get(url, params=params)
        data = res.json()["hourly"]
        print("[extract_weather] OK")
        return data

    # -------- VALIDATE & CLEAN --------
    @task()
    def validate_and_clean(aq_raw: dict, wx_raw: dict):

        df_aq = pd.DataFrame(aq_raw)
        df_wx = pd.DataFrame(wx_raw)

        df_aq.rename(columns={"time": "timestamp"}, inplace=True)
        df_wx.rename(columns={"time": "timestamp"}, inplace=True)

        df = pd.merge(df_aq, df_wx, on="timestamp", how="inner")
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        df.sort_values("timestamp", inplace=True)
        df.reset_index(drop=True, inplace=True)

        pollutant_cols = list(POLLUTANTS.keys())
        df.dropna(subset=pollutant_cols, how="all", inplace=True)

        # Clamp
        clamp_rules = {
            "pm2_5": (0, 500),
            "pm10": (0, 600),
            "ozone": (0, 400),
            "nitrogen_dioxide": (0, 300),
            "carbon_monoxide": (0, 15000),
            "temperature_2m": (-10, 55),
        }

        for col, (lo, hi) in clamp_rules.items():
            if col in df.columns:
                df[col] = df[col].clip(lo, hi)

        df[pollutant_cols] = df[pollutant_cols].ffill(limit=1)

        # 💥 FIX XCOM
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "records": df.to_dict(orient="records"),
            "row_count": len(df),
        }

    # -------- TRANSFORM --------
    @task()
    def transform_enrich(clean_data: dict):

        df = pd.DataFrame(clean_data["records"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # AQI Category
        def categorize(aqi):
            if aqi <= 20: return "Good"
            elif aqi <= 40: return "Fair"
            elif aqi <= 60: return "Moderate"
            else: return "Poor"

        df["aqi_category"] = df["european_aqi"].apply(categorize)

        df["hour"] = df["timestamp"].dt.hour

        df["health_risk_score"] = (
            df["pm2_5"] * 0.5 +
            df["pm10"] * 0.3 +
            df["ozone"] * 0.2
        )

        # 💥 FIX XCOM
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "records": df.to_dict(orient="records"),
            "row_count": len(df),
        }

    # -------- LOAD --------
    @task()
    def load_to_csv(data: dict):
        df = pd.DataFrame(data["records"])
        path = DATA_DIR / "air_quality.csv"
        df.to_csv(path, index=False)
        print(f"[load_to_csv] Saved → {path}")
        return str(path)

    # -------- AGGREGATE --------
    @task()
    def aggregate_stats(data: dict):
        df = pd.DataFrame(data["records"])

        stats = {
            "mean_pm25": df["pm2_5"].mean(),
            "max_ozone": df["ozone"].max(),
            "avg_temp": df["temperature_2m"].mean(),
        }

        print("[aggregate_stats]", stats)
        return stats

    # -------- FLOW --------
    aq = extract_airquality()
    wx = extract_weather()

    clean = validate_and_clean(aq, wx)
    enriched = transform_enrich(clean)

    load_to_csv(enriched)
    aggregate_stats(enriched)


dag = etl_air_quality()