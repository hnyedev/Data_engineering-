"""
API ETL Pipeline - Extract, Transform, Load

This DAG demonstrates a complete ETL pipeline using the TaskFlow API:
1. Extract: Fetch data from public APIs
2. Transform: Clean, enrich, and analyze data with pandas
3. Load: Save processed data to files

Author: Data Engineering Team
"""

from airflow.decorators import dag, task
from datetime import datetime, timedelta
import requests
import pandas as pd
import json
from pathlib import Path


@dag(
    dag_id='api_etl_pipeline',
    description='Complete ETL pipeline: Extract from APIs, Transform with pandas, Load to files',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'api', 'data-pipeline'],
    default_args={
        'owner': 'data-team',
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    }
)
def api_etl_pipeline():
    """
    Main ETL Pipeline DAG
    
    Flow: extract_users -> transform_users -> load_users
                        \                      /
          extract_posts -> transform_posts -> load_posts -> create_summary
    """
    
    @task
    def extract_users():
        """
        Extract user data from JSONPlaceholder API
        
        Returns:
            list: List of user dictionaries
        """
        print("📥 Extracting user data from API...")
        
        url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        users = response.json()
        print(f"✅ Extracted {len(users)} users")
        
        return users
    
    @task
    def extract_posts():
        """
        Extract posts data from JSONPlaceholder API
        
        Returns:
            list: List of post dictionaries
        """
        print("📥 Extracting posts data from API...")
        
        url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        posts = response.json()
        print(f"✅ Extracted {len(posts)} posts")
        
        return posts
    
    @task
    def transform_users(users_data: list):
        """
        Transform user data: flatten nested structures and add derived fields
        
        Args:
            users_data: Raw user data from API
            
        Returns:
            dict: Transformed data as records
        """
        print("🔄 Transforming user data...")
        
        # Convert to DataFrame
        df = pd.DataFrame(users_data)
        
        # Flatten nested structures
        df['company_name'] = df['company'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
        df['city'] = df['address'].apply(lambda x: x.get('city', '') if isinstance(x, dict) else '')
        df['lat'] = df['address'].apply(lambda x: x.get('geo', {}).get('lat', 0) if isinstance(x, dict) else 0)
        df['lng'] = df['address'].apply(lambda x: x.get('geo', {}).get('lng', 0) if isinstance(x, dict) else 0)
        
        # Add derived fields
        df['email_domain'] = df['email'].str.split('@').str[1]
        df['username_length'] = df['username'].str.len()
        
        # Select columns we want to keep
        columns = ['id', 'name', 'username', 'email', 'phone', 'website',
                   'company_name', 'city', 'lat', 'lng', 'email_domain', 'username_length']
        
        transformed_df = df[columns]
        
        print(f"✅ Transformed {len(transformed_df)} user records")
        
        # Return as dictionary for passing between tasks
        return {
            'data': transformed_df.to_dict('records'),
            'count': len(transformed_df)
        }
    
    @task
    def transform_posts(posts_data: list):
        """
        Transform posts data: add analytics and derived fields
        
        Args:
            posts_data: Raw posts data from API
            
        Returns:
            dict: Transformed data as records
        """
        print("🔄 Transforming posts data...")
        
        # Convert to DataFrame
        df = pd.DataFrame(posts_data)
        
        # Add analytics fields
        df['title_length'] = df['title'].str.len()
        df['body_length'] = df['body'].str.len()
        df['word_count'] = df['body'].str.split().str.len()
        
        # Categorize by length
        df['content_category'] = pd.cut(
            df['body_length'],
            bins=[0, 100, 200, float('inf')],
            labels=['short', 'medium', 'long']
        )
        
        # Convert category to string for JSON serialization
        df['content_category'] = df['content_category'].astype(str)
        
        print(f"✅ Transformed {len(df)} post records")
        
        return {
            'data': df.to_dict('records'),
            'count': len(df)
        }
    
    @task
    def load_users(transformed_data: dict, execution_date=None):
        """
        Load transformed user data to CSV and JSON files
        
        Args:
            transformed_data: Dictionary containing transformed user data
            execution_date: Airflow execution date (injected automatically)
        """
        print("💾 Loading user data to files...")
        
        # Create data directory if it doesn't exist
        data_dir = Path('/opt/airflow/data')
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert back to DataFrame
        df = pd.DataFrame(transformed_data['data'])
        
        # Generate date string for filename
        date_str = execution_date.strftime('%Y%m%d') if execution_date else datetime.now().strftime('%Y%m%d')
        
        # Save as CSV
        csv_path = data_dir / f'users_{date_str}.csv'
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved CSV: {csv_path}")
        
        # Save as JSON
        json_path = data_dir / f'users_{date_str}.json'
        with open(json_path, 'w') as f:
            json.dump(transformed_data['data'], f, indent=2)
        print(f"✅ Saved JSON: {json_path}")
        
        return str(csv_path)
    
    @task
    def load_posts(transformed_data: dict, execution_date=None):
        """
        Load transformed posts data to CSV and JSON files
        
        Args:
            transformed_data: Dictionary containing transformed posts data
            execution_date: Airflow execution date (injected automatically)
        """
        print("💾 Loading posts data to files...")
        
        # Create data directory
        data_dir = Path('/opt/airflow/data')
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert back to DataFrame
        df = pd.DataFrame(transformed_data['data'])
        
        # Generate date string for filename
        date_str = execution_date.strftime('%Y%m%d') if execution_date else datetime.now().strftime('%Y%m%d')
        
        # Save as CSV
        csv_path = data_dir / f'posts_{date_str}.csv'
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved CSV: {csv_path}")
        
        # Save as JSON
        json_path = data_dir / f'posts_{date_str}.json'
        with open(json_path, 'w') as f:
            json.dump(transformed_data['data'], f, indent=2)
        print(f"✅ Saved JSON: {json_path}")
        
        return str(csv_path)
    
    @task
    def create_summary(users_result: str, posts_result: str, execution_date=None):
        """
        Create a summary report combining all data
        
        Args:
            users_result: Path to users CSV file
            posts_result: Path to posts CSV file
            execution_date: Airflow execution date
        """
        print("📊 Creating summary report...")
        
        # Read the saved files
        users_df = pd.read_csv(users_result)
        posts_df = pd.read_csv(posts_result)
        
        # Create summary statistics
        summary = {
            'execution_date': execution_date.strftime('%Y-%m-%d') if execution_date else datetime.now().strftime('%Y-%m-%d'),
            'users': {
                'total_count': len(users_df),
                'unique_domains': users_df['email_domain'].nunique(),
                'top_domains': users_df['email_domain'].value_counts().head(3).to_dict(),
                'cities': users_df['city'].value_counts().to_dict()
            },
            'posts': {
                'total_count': len(posts_df),
                'by_user': posts_df['userId'].value_counts().head(5).to_dict(),
                'avg_length': float(posts_df['body_length'].mean()),
                'categories': posts_df['content_category'].value_counts().to_dict()
            }
        }
        
        # Save summary
        data_dir = Path('/opt/airflow/data')
        date_str = execution_date.strftime('%Y%m%d') if execution_date else datetime.now().strftime('%Y%m%d')
        summary_path = data_dir / f'summary_{date_str}.json'
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Summary report saved: {summary_path}")
        print(f"📊 Total users: {summary['users']['total_count']}")
        print(f"📊 Total posts: {summary['posts']['total_count']}")
        
        return summary
    
    # Define the pipeline flow
    # Extract phase (parallel)
    users_raw = extract_users()
    posts_raw = extract_posts()
    
    # Transform phase (parallel)
    users_transformed = transform_users(users_raw)
    posts_transformed = transform_posts(posts_raw)
    
    # Load phase (parallel)
    users_loaded = load_users(users_transformed)
    posts_loaded = load_posts(posts_transformed)
    
    # Summary phase (waits for all loads to complete)
    summary = create_summary(users_loaded, posts_loaded)


# Create the DAG instance
dag_instance = api_etl_pipeline()

