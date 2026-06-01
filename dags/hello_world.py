"""
Hello World DAG - Introduction to Airflow TaskFlow API

This DAG demonstrates the modern @task decorator syntax (TaskFlow API)
introduced in Airflow 2.0. This is the recommended way to write DAGs.

Key concepts:
- @task decorator automatically creates PythonOperator
- Return values are automatically passed via XCom
- Cleaner and more Pythonic syntax
"""

from airflow.decorators import dag, task
from datetime import datetime


@dag(
    dag_id='hello_world',
    description='A simple hello world DAG using TaskFlow API',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['tutorial', 'hello-world']
)
def hello_world_dag():
    """
    This is the DAG definition function.
    Tasks are defined as decorated functions inside.
    """
    
    @task
    def hello():
        """Print hello message and return data"""
        print("Hello from Airflow!")
        print("This task uses the @task decorator")
        return {"message": "Hello", "status": "success"}
    
    @task
    def goodbye(data: dict):
        """
        Receive data from previous task and print goodbye
        
        Args:
            data: Dictionary from previous task (passed automatically via XCom)
        """
        print(f"Received from hello task: {data}")
        print("Goodbye from Airflow!")
        return {"message": "Goodbye", "status": "complete"}
    
    # Define task dependencies
    # The return value of hello() is automatically passed to goodbye()
    hello_data = hello()
    goodbye_data = goodbye(hello_data)


# This creates the DAG
dag_instance = hello_world_dag() 