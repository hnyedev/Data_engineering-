# Airflow Lab - Quick Reference Cheat Sheet

## 🚀 Setup (First Time)

```bash
cd laboratories/4-ETL-Airflow-Orchestration
docker-compose up -d
```

Wait 1-2 minutes, then access: **http://localhost:8080**

## 🔐 Login

```
Username: airflow
Password: airflow
```

## 📊 View Your DAGs

After login, you'll see:
- `hello_world` - Simple 2-task example
- `api_etl_pipeline` - Complete ETL pipeline

**Enable a DAG**: Click the toggle switch to turn it ON

**Run a DAG**: Click the Play button → "Trigger DAG"

## 🔍 Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop Airflow
docker-compose down

# Fresh restart (deletes data)
docker-compose down -v && docker-compose up -d

# Check status
docker-compose ps

# View data files
ls -la data/raw/
ls -la data/processed/
ls -la data/analytics/
```

## 📁 Where Things Are

| Path | What's There |
|------|-------------|
| `dags/` | Your DAG Python files |
| `logs/` | Task execution logs |
| `data/raw/` | Raw API responses (JSON) |
| `data/processed/` | Transformed data (CSV + JSON) |
| `data/analytics/` | Summary reports (JSON) |

## 🛠️ Debugging

**Task failed?**
1. Click on the failed task (red box)
2. Click "Log" button
3. Read the error message
4. Fix your code
5. Re-run the DAG

**DAG not appearing?**
```bash
# Check for errors
docker-compose logs webserver | grep -i error
docker-compose logs scheduler | grep -i error
```

## 📝 TaskFlow API Syntax

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id='my_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
)
def my_pipeline():
    
    @task
    def extract():
        # Your extraction code
        return data
    
    @task
    def transform(data):
        # Your transformation code
        return transformed_data
    
    @task
    def load(data):
        # Your load code
        pass
    
    # Define flow
    raw = extract()
    clean = transform(raw)
    load(clean)

dag_instance = my_pipeline()
```

## 🌐 API Endpoints (In DAGs)

**JSONPlaceholder** (used in examples):
- Users: https://jsonplaceholder.typicode.com/users
- Posts: https://jsonplaceholder.typicode.com/posts
- Comments: https://jsonplaceholder.typicode.com/comments

**Weather APIs** (for assignments):
- Open-Meteo: https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true
- No API key required!

## 🎨 Airflow UI Views

| View | What It Shows |
|------|---------------|
| **DAGs** | List of all workflows |
| **Graph** | Visual task dependencies |
| **Tree** | Historical runs |
| **Gantt** | Task timing |
| **Code** | DAG source code |
| **Log** | Task execution logs |

## 🚦 Task Colors

| Color | Meaning |
|-------|---------|
| 🟢 Green | Success |
| 🔴 Red | Failed |
| 🟡 Yellow | Running |
| ⚪ Light Gray | Not yet run |
| ⬛ Dark Gray | Skipped |
| 🟣 Purple | Upstream failed |

## 💡 Pro Tips

1. **Start Small**: Test your tasks individually before connecting them
2. **Use Logs**: The log view is your best friend for debugging
3. **Add Print Statements**: Use `print()` liberally in your tasks
4. **Check Data**: Verify files are created in `data/` directory
5. **Read Examples**: Study `hello_world.py` and `api_etl_pipeline.py`

## 🆘 Common Issues

**Port 8080 in use?**
```bash
# Kill the process or change port in docker-compose.yml
lsof -i :8080
kill -9 <PID>
```

**Database not initialized?**
```bash
# Rarely needed with auto-init, but if needed:
./init-airflow.sh
```

**Import error in DAG?**
```bash
# Check Python syntax
python dags/my_dag.py
```

**Need to add Python package?**
```dockerfile
# Edit Dockerfile, add to RUN pip install line
# Then rebuild:
docker-compose down
docker-compose build
docker-compose up -d
```

## 📚 Documentation

- **README.md** - Complete guide with exercises
- **QUICKSTART.md** - Fast setup reference
- **DELIVERABLES.md** - Assignment requirements
- **CREDENTIALS.md** - Login info
- **LAB-OVERVIEW.md** - Teaching guide
- **SUMMARY.md** - Complete overview
- **CHEATSHEET.md** - This file

## 🎓 Assignment Checklist

- [ ] Run `hello_world` DAG successfully
- [ ] Run `api_etl_pipeline` DAG successfully
- [ ] Explore generated data files
- [ ] Create custom weather ETL DAG
- [ ] Test your custom DAG
- [ ] Document your work
- [ ] Take screenshots
- [ ] Submit deliverables

## 🌟 Quick Wins

Want to feel like an Airflow pro? Try these:

1. **Trigger a DAG manually** and watch it run
2. **View the Graph view** - see the visual workflow
3. **Click on a task** and read its logs
4. **Find a data file** in `data/processed/`
5. **Modify a print statement** in `hello_world.py` and re-run

---

**Need more help?** Read [README.md](README.md) or ask your instructor!

**Login**: http://localhost:8080 (`airflow` / `airflow`)

