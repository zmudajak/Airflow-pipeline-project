
# import libraries and etl function
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from airflow_etl import run_api_etl

# define default arguments for airflow DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 11, 8),
    "email": ['airflow@example.com'],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

# define DAG
dag = DAG(
    "api_etl_dag",
    default_args=default_args,
    description="My etl code"
)

# define etl task in DAG
run_etl = PythonOperator(
    task_id="complete_etl",
    python_callable=run_api_etl,
    dag=dag,
)

# run task
run_etl
