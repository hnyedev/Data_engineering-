# Data Engineering Portfolio

A collection of real data engineering projects and hands-on practices — covering the full spectrum from pipeline orchestration and real-time streaming to cloud deployment and business intelligence.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/Amazon%20AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Metabase](https://img.shields.io/badge/Metabase-509EE3?style=for-the-badge&logo=metabase&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

---

## About

Data engineer with hands-on experience building end-to-end data systems. The work in this repository spans pipeline orchestration with Apache Airflow, real-time dashboards backed by Kafka, cloud infrastructure managed with Terraform, data warehousing with proper layer separation (Bronze → Silver → Gold), business intelligence with Metabase, and ETL pipelines consuming both REST APIs and document databases like MongoDB. Every project here was built and deployed from scratch.

---

## Projects

### ETL Orchestration with Apache Airflow

A fully containerized Airflow 2.8.1 environment using the modern TaskFlow API (`@task` decorators). Includes three production-style DAGs:

| DAG | Source | Description |
|-----|--------|-------------|
| `api_etl_pipeline` | JSONPlaceholder REST API | Parallel extract of users + posts → pandas transform → CSV/JSON load with summary report |
| `ETL_airquality` | Open-Meteo Air Quality API | Daily ingestion of PM2.5, PM10, O3, NO2, CO and AQI for Mérida, Yucatán with data validation and forward-fill |
| `4etl_ocean` | Open-Meteo Marine API | Hourly Gulf of Mexico marine conditions — wave height, period, direction, current speed |

**Stack:** Apache Airflow 2.8.1 · PostgreSQL 13 · Docker Compose · Python · Pandas · LocalExecutor

---

### Kafka Real-Time Dashboard — Cloud Deployment on AWS

A multi-page operational dashboard deployed live on AWS using a fully automated infrastructure-as-code workflow. Data is streamed through Apache Kafka and visualized in Streamlit across five domain dashboards: Operations, Energy, Security, Market, and Emerging Technology.

Infrastructure is defined entirely in Terraform and deployed to AWS Free Tier — EC2 instance, security group, and Elastic IP — with a Docker-based deployment pipeline via `deploy.sh`.

**Stack:** Apache Kafka · Streamlit · Plotly · Terraform · AWS EC2 · Docker · Python

```
dc-dashboard/
├── app.py
├── pages/          # 5 domain dashboards
├── utils/          # data_loader, charts
└── infra/          # Terraform (EC2 + EIP + Security Group)
```

---

### Data Warehouse + Metabase BI

A complete data warehousing project built on top of a MongoDB ETL extraction, implementing proper data layer architecture and SQL schema design. Data is processed and stored in PostgreSQL following the medallion pattern, then surfaced through Metabase for business intelligence analysis.

Applied to real Yucatán public safety data — raw ingestion through cleaning, normalization, and warehousing.

**Stack:** MongoDB · PostgreSQL · Metabase · Docker Compose · Python · SQL

```
Metabase/
├── docker-compose.yml      # PostgreSQL + Metabase services
├── sql_scripts/            # Bronze schema, warehouse schema, raw tables
│   ├── create_bronze_schema.sql
│   ├── create_warehouse_db.sql
│   └── create_raw_insecurity_table.sql
└── raw_data/               # Source dataset (Yucatán insecurity data)
```

Data layer structure:

| Layer | Schema | Purpose |
|-------|--------|---------|
| Bronze | `bronze` | Raw ingestion, no transformations |
| Silver | — | Cleaning, type casting, deduplication |
| Gold | Warehouse | Aggregated, analytics-ready tables |

---

### YouTube Channel Analytics Scraper

An ETL pipeline that consumes the YouTube Data API v3 to extract video-level statistics across multiple channel categories (Gaming, Tech, Education, Entertainment, Music). Includes data quality checks, statistical analysis, and a full visualization suite.

Outputs processed CSVs per team and six analytical plots covering view distributions, correlation heatmaps, top performers, and duration analysis.

**Stack:** YouTube Data API v3 · Pandas · Matplotlib · Seaborn · Plotly · python-dotenv

> Credentials loaded from environment variables via `.env` — no keys hardcoded.

---

### Pokémon API — ETL Practice

A focused ETL exercise using the public PokéAPI. Demonstrates the extract-transform-load pattern at its clearest: fetch raw JSON from the REST API, filter and reshape the payload (name, height, weight, type, moves, image), and persist each record as a structured JSON file.

**Stack:** Python · Requests · REST API

---

## Skills at a Glance

| Area | Tools & Technologies |
|------|---------------------|
| **Pipeline Orchestration** | Apache Airflow 2.8.1, TaskFlow API, DAG design, scheduling |
| **Streaming** | Apache Kafka, real-time data ingestion |
| **Databases** | PostgreSQL, MongoDB, SQL schema design |
| **Data Warehousing** | Medallion architecture (Bronze/Silver/Gold), ETL layer separation |
| **Data Processing** | Pandas, NumPy, data cleaning, validation, aggregation |
| **Visualization & BI** | Streamlit, Plotly, Metabase, Matplotlib, Seaborn |
| **Infrastructure** | Docker, Docker Compose, Terraform, AWS EC2 |
| **Cloud** | AWS Free Tier deployment, Elastic IP, security groups |
| **API Integration** | REST APIs, YouTube Data API v3, Open-Meteo, PokéAPI |
| **Languages** | Python, SQL, HCL (Terraform) |

---

## Repository Structure

```
Pipelines/
├── dags/                    # Airflow DAGs (ETL pipelines)
│   ├── api_etl_pipeline.py
│   ├── ETL_airquality.py
│   └── 4etl_ocean.py
├── dc-dashboard/            # Kafka dashboard — AWS cloud deployment
│   ├── pages/
│   ├── utils/
│   └── infra/               # Terraform infrastructure
├── Metabase/                # Data warehouse + BI platform
│   ├── sql_scripts/
│   └── raw_data/
├── Youtube scraping/        # YouTube API ETL + analysis
├── pokemonapi/              # REST API ETL practice
├── docker-compose.yml       # Airflow stack
└── Dockerfile               # Custom Airflow image
```

---

## Running the Projects

### Airflow Stack
```bash
docker-compose up --build
# UI: http://localhost:8080  |  user: airflow  |  pass: airflow
```

### Metabase + PostgreSQL
```bash
cp Metabase/.env.example Metabase/.env
# Edit .env with your credentials
cd Metabase && docker-compose up -d
# Metabase: http://localhost:3000
```

### DC Dashboard (local)
```bash
cd dc-dashboard
pip install -r requirements.txt
streamlit run app.py
```

### YouTube Scraper
```bash
cd "Youtube scraping"
echo "API_KEY=your_youtube_api_key" > .env
python scrape_youtube.py
```
