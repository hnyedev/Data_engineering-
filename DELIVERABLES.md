# Laboratory 4 - Deliverables

## 📝 Assignment Overview

Create a complete ETL pipeline using Apache Airflow's TaskFlow API. This assignment demonstrates your understanding of workflow orchestration, API integration, and data transformation.

## 🎯 Requirements

### Part 1: Environment Setup and Exploration (25 points)

#### Deliverable 1.1: Hello World DAG Execution
- Screenshot showing successful execution of `hello_world` DAG
- Graph view with both tasks in green (success)
- Include timestamp

#### Deliverable 1.2: ETL Pipeline Execution  
- Screenshot of `api_etl_pipeline` Graph view showing all tasks completed
- Screenshot showing the generated data files in `/opt/airflow/data`
- Copy of the `summary_YYYYMMDD.json` file content

### Part 2: Understanding the Pipeline (25 points)

#### Deliverable 2.1: Data Flow Analysis
Write a brief report (300-500 words) explaining:

1. **Extract Phase**: 
   - Which APIs are used?
   - How many records are extracted?
   - Why are extract tasks run in parallel?

2. **Transform Phase**:
   - What transformations are applied to user data?
   - What analytics are added to posts data?
   - How is pandas used in the transformation?

3. **Load Phase**:
   - What file formats are created?
   - Where are files saved?
   - Why save in multiple formats?

4. **Data Flow**:
   - How is data passed between tasks?
   - What is XCom and how is it used?
   - Draw a simple diagram showing task dependencies

### Part 3: Custom DAG Creation (50 points)

Create a new DAG file: `dags/weather_etl.py`

#### Requirements:

**Functional Requirements:**
1. Extract weather data from a public API (Open-Meteo, WeatherAPI, etc.)
2. Transform the data:
   - Convert temperature units (e.g., Celsius to Fahrenheit)
   - Add derived fields (feels_like, temp_category, etc.)
   - Create summary statistics
3. Load data to CSV and JSON files with date in filename
4. Minimum 3 tasks using TaskFlow API (`@task` decorator)

**Technical Requirements:**
- Use `@dag` and `@task` decorators (TaskFlow API)
- Include proper docstrings for DAG and each task
- Add helpful print statements with emojis (like the example)
- Include error handling (try/except)
- Use type hints (e.g., `def transform(data: dict) -> dict:`)
- Schedule: `@daily` or `@hourly`
- Tag with `['weather', 'etl', 'student']`
- Set `catchup=False`

**Code Quality:**
- Clean, readable code
- Meaningful variable and function names
- Comments explaining complex logic
- PEP 8 style compliance

#### What to Submit:

1. **Code**: `weather_etl.py` file
2. **Screenshot**: Graph view showing successful execution
3. **Data Files**: Sample CSV and JSON output files
4. **Documentation**: Brief explanation (200-300 words) covering:
   - API chosen and why
   - Transformations applied
   - Challenges faced and solutions
   - Interesting insights from the data

## 📁 Submission Structure

Create the following structure:

```
students/[YOUR-ID]-[YOUR-NAME]/4-ETL-Airflow-Orchestration/
├── screenshots/
│   ├── 1.1-hello-world-success.png
│   ├── 1.2-etl-pipeline-graph.png
│   ├── 1.3-data-files-listing.png
│   └── 3.1-weather-dag-success.png
├── reports/
│   ├── data-flow-analysis.md
│   ├── weather-dag-documentation.md
│   └── summary_YYYYMMDD.json
├── code/
│   └── weather_etl.py
└── data-samples/
    ├── weather_YYYYMMDD.csv
    └── weather_YYYYMMDD.json
```

## 📊 Grading Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Part 1: Setup** | 25 | |
| - Hello World execution | 10 | Clear screenshot, successful run |
| - ETL Pipeline execution | 10 | All tasks completed, files generated |
| - Data files | 5 | Files correctly created and accessible |
| **Part 2: Analysis** | 25 | |
| - Extract phase understanding | 6 | Accurate explanation of extraction process |
| - Transform phase understanding | 6 | Clear description of transformations |
| - Load phase understanding | 6 | Understands file creation and formats |
| - Data flow diagram | 7 | Clear visualization of task dependencies |
| **Part 3: Custom DAG** | 50 | |
| - Code functionality | 20 | DAG runs successfully, meets requirements |
| - TaskFlow API usage | 10 | Proper use of @task decorators |
| - Code quality | 10 | Clean code, good practices, documentation |
| - Documentation | 10 | Clear explanation of design decisions |
| **Total** | **100** | |

### Detailed Scoring for Custom DAG (Part 3)

#### Code Functionality (20 points)
- **18-20**: Runs perfectly, all requirements met, extra features
- **15-17**: Runs well, all core requirements met
- **12-14**: Runs with minor issues, most requirements met
- **0-11**: Doesn't run or major requirements missing

#### TaskFlow API Usage (10 points)
- **9-10**: Excellent use of decorators, type hints, clean syntax
- **7-8**: Good use of TaskFlow API
- **5-6**: Basic TaskFlow API, some issues
- **0-4**: Incorrect or minimal use of TaskFlow API

#### Code Quality (10 points)
- **9-10**: Excellent code style, well-documented, best practices
- **7-8**: Good code quality, adequate documentation
- **5-6**: Acceptable code, minimal documentation
- **0-4**: Poor code quality, no documentation

#### Documentation (10 points)
- **9-10**: Comprehensive, insightful, well-written
- **7-8**: Good explanation, covers main points
- **5-6**: Basic explanation, missing some details
- **0-4**: Incomplete or unclear documentation

## 🌟 Bonus Opportunities (+10 points)

Earn extra credit by implementing:

1. **Multiple Data Sources** (+3 points): Extract from 2+ different APIs
2. **Data Validation Task** (+3 points): Add a task that validates data quality
3. **Advanced Transformations** (+2 points): Complex pandas operations, aggregations
4. **Email Notifications** (+2 points): Configure email alerts (even if test mode)
5. **Error Handling** (+2 points): Comprehensive error handling with retries
6. **Data Visualization** (+3 points): Generate plots/charts from the data

## ⏰ Submission Deadline

**Due Date**: [TO BE ANNOUNCED BY INSTRUCTOR]

**Late Submission Policy**:
- Up to 24 hours late: -10%
- 24-48 hours late: -25%
- More than 48 hours late: -50%

## 📤 How to Submit

### Method 1: Git Repository (Recommended)

```bash
# Navigate to your student directory
cd students/[YOUR-ID]-[YOUR-NAME]

# Add your work
git add 4-ETL-Airflow-Orchestration/

# Commit
git commit -m "Lab 4: Airflow ETL Pipeline - [Your Name]"

# Push
git push origin [your-branch]

# Create Pull Request on GitHub
```

### Method 2: Archive Upload (Alternative)

1. Zip your entire submission directory
2. Name it: `[YOUR-ID]-Lab4-Airflow.zip`
3. Upload to course platform

## ✅ Pre-Submission Checklist

Before submitting, ensure:

- [ ] All required screenshots included
- [ ] Screenshots show timestamps
- [ ] Weather DAG file is properly formatted
- [ ] Weather DAG runs successfully (tested!)
- [ ] All documentation files included
- [ ] Data sample files included
- [ ] File naming follows requirements
- [ ] Git commits have meaningful messages
- [ ] No sensitive information (API keys should use environment variables)
- [ ] README or documentation explains setup if needed

## 💡 Tips for Success

1. **Start Early**: Don't wait until the last day
2. **Test Frequently**: Run your DAG multiple times to ensure reliability
3. **Read Logs**: Airflow logs are your best debugging tool
4. **Use Examples**: Reference the provided `api_etl_pipeline.py`
5. **Ask Questions**: Use office hours if stuck
6. **Document as You Go**: Write documentation while coding
7. **Handle Errors**: Add try/except blocks for API calls
8. **Test Incrementally**: Test each task before connecting them

## 🆘 Common Issues and Solutions

### Issue: DAG not appearing in UI
**Solution**: Check for import errors
```bash
docker-compose exec webserver airflow dags list-import-errors
```

### Issue: Task fails with import error
**Solution**: Add required package to Dockerfile and rebuild
```bash
docker-compose build
docker-compose down
docker-compose up -d
```

### Issue: API requires authentication
**Solution**: Use environment variables or choose a different API

### Issue: Data not saving correctly
**Solution**: Check file paths and permissions, use absolute paths

## 📚 Recommended APIs (No Auth Required)

- **Open-Meteo**: https://open-meteo.com/en/docs
- **CoinGecko**: https://www.coingecko.com/en/api/documentation
- **REST Countries**: https://restcountries.com/
- **JSONPlaceholder**: https://jsonplaceholder.typicode.com/
- **Advice Slip**: https://api.adviceslip.com/

## 🎓 Learning Outcomes

By completing this assignment, you will demonstrate:

✅ Understanding of Apache Airflow and DAGs  
✅ Proficiency with TaskFlow API and decorators  
✅ Ability to integrate external APIs  
✅ Skills in data transformation with pandas  
✅ Knowledge of workflow orchestration patterns  
✅ Capability to debug and troubleshoot pipelines  

## 📞 Questions?

- **Technical Issues**: Post in course forum with error logs
- **Clarifications**: Email instructor or ask during office hours
- **General Questions**: Check README.md and Airflow documentation first

---

**Good Luck! 🚀**

*Remember: The goal is learning. Focus on understanding the concepts, not just completing the assignment. Airflow skills are highly valued in the data engineering industry!*

