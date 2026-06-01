# Lab 4: Apache Airflow - ETL Pipeline Orchestration

## 📚 Complete Lab Overview

This laboratory teaches Apache Airflow fundamentals using the modern **TaskFlow API** with `@task` decorators. Students learn to build production-grade ETL pipelines that extract data from APIs, transform it with pandas, and load it to files.

## ✅ What's Included

### Infrastructure
- ✅ Docker Compose setup with Airflow 2.8.1
- ✅ PostgreSQL backend for metadata
- ✅ Custom Dockerfile with pandas and requests
- ✅ LocalExecutor for parallel task execution
- ✅ Data directory for processed files

### Example DAGs

#### 1. `hello_world.py` - Introduction
- Simple 2-task pipeline
- Demonstrates TaskFlow API syntax
- Shows data passing between tasks
- Perfect for first-time users

#### 2. `api_etl_pipeline.py` - Complete ETL
- Extracts data from JSONPlaceholder API
- Transforms with pandas (flatten, enrich, analyze)
- Loads to CSV and JSON files
- Creates summary reports
- **5 tasks total**: 2 extract (parallel), 2 transform (parallel), 1 summary
- Demonstrates real-world ETL patterns

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main lab guide with exercises |
| `QUICKSTART.md` | 5-minute setup guide |
| `DELIVERABLES.md` | Assignment requirements and rubric |
| `LAB-OVERVIEW.md` | This file - complete overview |

## 🎯 Learning Objectives

Students will learn to:
1. ✅ Understand Apache Airflow and workflow orchestration
2. ✅ Use the TaskFlow API with `@task` decorators
3. ✅ Build ETL pipelines (Extract, Transform, Load)
4. ✅ Integrate external REST APIs
5. ✅ Transform data with pandas
6. ✅ Manage task dependencies and parallel execution
7. ✅ Monitor and debug pipelines
8. ✅ Follow data engineering best practices

## 🔑 Key Features

### Modern TaskFlow API

This lab teaches the **modern way** to write Airflow DAGs:

```python
@dag(dag_id='my_pipeline', start_date=datetime(2024, 1, 1))
def my_pipeline():
    
    @task
    def extract():
        return requests.get("https://api.example.com/data").json()
    
    @task
    def transform(data: list):
        df = pd.DataFrame(data)
        return df.to_dict('records')
    
    @task
    def load(data: dict):
        pd.DataFrame(data).to_csv('/opt/airflow/data/output.csv')
    
    data = extract()
    transformed = transform(data)
    load(transformed)

dag_instance = my_pipeline()
```

**Benefits:**
- ✅ Cleaner syntax than traditional operators
- ✅ Automatic XCom handling
- ✅ Type hints for better IDE support
- ✅ Pythonic and intuitive
- ✅ Industry best practice (Airflow 2.x+)

### Real ETL Pipeline

The `api_etl_pipeline.py` demonstrates:

**Extract Phase (Parallel)**
- `extract_users()` - Fetch user data
- `extract_posts()` - Fetch posts data

**Transform Phase (Parallel)**
- `transform_users()` - Flatten nested JSON, add derived fields
- `transform_posts()` - Calculate analytics, categorize content

**Load & Summary Phase (Sequential)**
- `load_users()` - Save to CSV and JSON
- `load_posts()` - Save to CSV and JSON  
- `create_summary()` - Generate combined report

**Data Flow:**
```
extract_users → transform_users → load_users ↘
                                                create_summary
extract_posts → transform_posts → load_posts ↗
```

## 📊 Assignment Structure

### Part 1: Setup & Exploration (25 points)
- Run `hello_world` DAG
- Run `api_etl_pipeline` DAG
- Verify data files created

### Part 2: Understanding (25 points)
- Analyze data flow
- Explain each phase (Extract, Transform, Load)
- Document task dependencies
- Create simple diagram

### Part 3: Create Custom DAG (50 points)
- Build weather ETL pipeline
- Use TaskFlow API (`@task` decorators)
- Extract from weather API
- Transform data (convert units, add fields)
- Load to CSV/JSON files
- Document design decisions

## 🛠️ Technical Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Orchestration | Apache Airflow | 2.8.1 |
| Database | PostgreSQL | 13 |
| Python | Python | 3.11 |
| Data Processing | Pandas | 2.1.4 |
| HTTP Client | Requests | 2.31.0 |
| Container | Docker | 20.10+ |
| Orchestration | Docker Compose | v3.8 |

## 📁 Directory Structure

```
4-ETL-Airflow-Orchestration/
├── docker-compose.yml          # Services: postgres, webserver, scheduler
├── Dockerfile                  # Custom image with pandas, requests
├── .gitignore                  # Ignore logs, data, cache
│
├── Documentation:
│   ├── README.md              # Main guide (exercises, concepts)
│   ├── QUICKSTART.md          # Fast setup guide
│   ├── DELIVERABLES.md        # Assignment requirements
│   └── LAB-OVERVIEW.md        # This file
│
├── dags/                       # Airflow DAG files
│   ├── hello_world.py         # Introduction to TaskFlow API
│   └── api_etl_pipeline.py    # Complete ETL example
│
├── logs/                       # Airflow logs (auto-created)
└── data/                       # Processed data files (auto-created)
```

## 🚀 Quick Start Commands

### For Students (ONE COMMAND!)

```bash
cd laboratories/4-ETL-Airflow-Orchestration
docker-compose up -d
```

**That's it!** Everything is automatic:
- ✅ Builds custom image
- ✅ Initializes database  
- ✅ Creates admin user
- ✅ Starts all services

### Access

**Web UI**: http://localhost:8080  
**Login**: `airflow` / `airflow`

### Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Fresh start (deletes all data)
docker-compose down -v
docker-compose up -d
```

## 🎓 Pedagogical Approach

### Progressive Learning
1. **Hello World** - Understand basic concepts
2. **Example Pipeline** - See complete implementation
3. **Custom DAG** - Apply knowledge independently

### Hands-On Focus
- Real APIs (JSONPlaceholder, Open-Meteo)
- Real transformations (pandas operations)
- Real file outputs (CSV, JSON)
- No mocks or simulations

### Best Practices Demonstrated
- ✅ TaskFlow API (modern Airflow 2.x)
- ✅ Type hints for better code
- ✅ Docstrings and comments
- ✅ Error handling
- ✅ Meaningful logging
- ✅ Clean code structure
- ✅ Parallel task execution
- ✅ Data validation

## 📈 Expected Time Investment

| Activity | Time | Cumulative |
|----------|------|------------|
| Setup environment | 15-20 min | 20 min |
| Run hello_world DAG | 15 min | 35 min |
| Run api_etl_pipeline | 20 min | 55 min |
| Analyze and document | 45 min | 1h 40min |
| Create custom weather DAG | 2-3 hours | 4-5 hours |
| Documentation | 30-45 min | 5-6 hours |
| **Total** | **5-6 hours** | |

## 🌟 Key Differentiators

### Why This Lab is Effective

1. **Modern Syntax**: TaskFlow API, not outdated traditional operators
2. **Simple Setup**: Docker Compose, one command to start
3. **Real Skills**: Industry-standard tools and patterns
4. **Practical**: APIs, pandas, file I/O - real data engineering
5. **Well-Documented**: 4 comprehensive guides
6. **Clear Assignment**: Detailed rubric and requirements
7. **Extensible**: Easy to add more complexity

### What Students Gain

**Technical Skills:**
- Apache Airflow proficiency
- TaskFlow API expertise  
- ETL pipeline design
- pandas data transformation
- API integration
- Docker basics
- Debugging and troubleshooting

**Professional Skills:**
- Workflow orchestration concepts
- Data engineering patterns
- Code documentation
- Technical writing
- Problem-solving

## 💼 Industry Relevance

### Companies Using Airflow
- Airbnb (created Airflow)
- Adobe, Twitter, Lyft, Uber
- PayPal, Square, Stripe
- ING, Netflix, Reddit
- Thousands more...

### Job Market Value
- **Data Engineer**: Core requirement
- **Data Scientist**: Workflow automation
- **ML Engineer**: Model training pipelines
- **Analytics Engineer**: Data transformations

## 🎯 Success Metrics

Students successfully complete the lab when they:
- ✅ Run both example DAGs successfully
- ✅ Understand the ETL pipeline flow
- ✅ Create a working custom DAG
- ✅ Use TaskFlow API correctly
- ✅ Generate and analyze data files
- ✅ Document their work clearly

## 🔧 Troubleshooting

### Common Issues

**Issue**: DAG not appearing  
**Solution**: `docker-compose exec webserver airflow dags list-import-errors`

**Issue**: Port 8080 in use  
**Solution**: Change port in docker-compose.yml to 8081:8080

**Issue**: Permission errors  
**Solution**: `chmod -R 755 dags logs data`

**Issue**: Task fails  
**Solution**: Check logs in Airflow UI, click task → Log

## 📚 Learning Resources

**Official Docs:**
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [TaskFlow API Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)

**Free APIs:**
- [Open-Meteo](https://open-meteo.com/) - Weather (no auth)
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Test data
- [REST Countries](https://restcountries.com/) - Country data

## ✅ Quality Checklist

This lab provides:
- ✅ Modern Airflow 2.x TaskFlow API
- ✅ Complete working examples
- ✅ Clear documentation
- ✅ Practical exercises
- ✅ Detailed assignment rubric
- ✅ Real-world patterns
- ✅ No linting errors
- ✅ Ready to use immediately

## 🎉 Summary

This laboratory offers a **complete, modern, hands-on introduction to Apache Airflow** using industry best practices. Students learn by doing - setting up Airflow, running examples, and building their own ETL pipeline. The TaskFlow API focus prepares them for real-world data engineering work.

**Key Strengths:**
- ✨ Modern TaskFlow API (not outdated syntax)
- ✨ Simple Docker setup
- ✨ Real ETL pipeline examples
- ✨ Comprehensive documentation
- ✨ Clear learning path
- ✨ Industry-relevant skills

**Perfect for:**
- Data engineering courses
- Data science bootcamps
- Self-paced learning
- Corporate training

---

**Lab Status**: ✅ Complete and Ready  
**Version**: 1.0  
**Created**: October 2025  
**Maintained By**: Data Engineering Team

*This lab represents industry best practices for teaching Apache Airflow in 2025 and beyond.*

