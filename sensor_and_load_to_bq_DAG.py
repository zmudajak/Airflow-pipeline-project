from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectSensor
from airflow.operators.python_operator import PythonOperator
from airflow_etl import create_temp_table, load_data_to_temp, load_data_to_final, delete_temp_table

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gcp_data_sensor_dag',
    default_args=default_args,
    description='DAG to sensor GCP bucket file'
)

# Define a Google Cloud Storage sensor to monitor a specific file
file_sensor_task = GoogleCloudStorageObjectSensor(
    task_id='file_sensor_task',
    bucket='airflow-etl-bucket',
    object='currency_data.csv',
    mode='poke',
    timeout=600,  # Adjust timeout as needed
    poke_interval=60,  # Adjust poke_interval as needed
    dag=dag
)

# Define next steps depending on file sensor task
create_temp_table_task = PythonOperator(
    task_id='create_temp_table_task',
    python_callable=create_temp_table,
    dag=dag
)

load_data_to_temp_task = PythonOperator(
    task_id='load_data_to_temp_task',
    python_callable=load_data_to_temp,
    dag=dag
)

load_data_to_final_task = PythonOperator(
    task_id='load_data_to_final_task',
    python_callable=load_data_to_final,
    dag=dag
)

delete_temp_table_task = PythonOperator(
    task_id='delete_temp_table_task',
    python_callable=delete_temp_table,
    dag=dag
)

file_sensor_task >> create_temp_table_task >> load_data_to_temp_task \
>> load_data_to_final_task >> delete_temp_table_task