import os
from datetime import timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
import pandas as pd
from utils.file_utils import save_files
from utils.generate_histograms import generate_histograms
# from matplotlib import pyplot as plt

# Database connection string
# Replace with your actual database connection details
CONNECTION_STRING = "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"

# Set up SQLAlchemy engine
engine = create_engine(CONNECTION_STRING)


@dag(
    schedule_interval=timedelta(days=1),
    start_date=days_ago(0),
    default_args={'owner':'airflow', 'retries':1, 'retry_delay':timedelta(minutes=5)},
    tags=['data_processing'],
    catchup=False
)

def data_processing_and_cleaning():

    @task(task_id='load_data_task')
    def load_data():
        # The dataset for competition
        train = pd.read_csv('/opt/airflow/data/train.csv')
        test = pd.read_csv('/opt/airflow/data/test.csv')
        
        # Load data into the database
        train.to_sql('train_table', engine, if_exists='replace', index=False)
        test.to_sql('test_table', engine, if_exists='replace', index=False)

    @task(task_id='clean_data_task')
    def clean_data():
        # Read data from the database
        train = pd.read_sql('SELECT * FROM train_table', engine)
        test = pd.read_sql('SELECT * FROM test_table', engine)

        # Drop the 'id' column 
        train = train.drop(['id'], axis=1)
        test = test.drop(['id'], axis=1)
        train = train.drop_duplicates()

        # Update cleaned data back to the database
        train.to_sql('train_clean_table', engine, if_exists='replace', index=False)
        test.to_sql('test_clean_table', engine, if_exists='replace', index=False)

    @task(task_id='preprocess_data_task')
    def preprocess_data():
        train = pd.read_sql('SELECT * FROM train_clean_table', engine)
        
        Y = train['smoking']
        X = train.drop(['smoking'], axis=1)

        X.to_csv('/opt/airflow/data/X.csv', sep=',', index=False)
        Y.to_csv('/opt/airflow/data/Y.csv', sep=',', index=False)

    @task(task_id='save_data_task')
    def plot_data():
        X = pd.read_csv('/opt/airflow/data/X.csv')
        Y = pd.read_csv('/opt/airflow/data/Y.csv')

        generate_histograms(X, '/opt/airflow/plots')
        generate_histograms(Y, '/opt/airflow/plots')

    loaded_data = load_data()
    cleaned_data = clean_data()
    preprocessed_data = preprocess_data()
    plot_data() 


dag = data_processing_and_cleaning()