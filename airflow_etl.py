#  importing libraries

import requests
from datetime import datetime
from datetime import timedelta
import pandas as pd
import gcsfs
from google.cloud import bigquery

def run_api_etl():
    # setting historical data to download currency exchange data
    today = datetime.now()
    historical_date = (today - timedelta(days=90)).strftime("%Y-%m-%d")

    # getting the data using requests.get function from Free Frankfurter Currency Exchange API endpoint
    url = f"http://api.frankfurter.app/{historical_date}.."
    data = requests.get(url=url)

    # converting data to pandas dataframe object and saving data in .csv format
    df = pd.DataFrame(data.json()['rates'])
    df = df.transpose()
    df = df['USD']
    df.to_csv("gs://airflow-etl-bucket/currency_data.csv", header=False)

def create_temp_table():

    table_id = 'temp'
    dataset_id = 'currency'

    # Replace 'your-project-id' with your actual project ID
    project_id = 'your-project-id'

    # Initialize a BigQuery client
    client = bigquery.Client(project=project_id)

    # Define the schema for table
    schema = [
        bigquery.SchemaField('date', 'DATE'),
        bigquery.SchemaField('USD', 'FLOAT')
    ]

    # Create a table reference
    table_ref = client.dataset(dataset_id).table(table_id)

    # Specify the table schema when creating the table
    table = bigquery.Table(table_ref, schema=schema)

    # Create the table
    client.create_table(table)


def load_data_to_temp():

    table_id = 'temp'
    dataset_id = 'currency'

    # Replace 'your-project-id' with your actual project ID
    project_id = 'your-project-id'

    # Initialize a BigQuery client
    client = bigquery.Client(project=project_id)

    # Specify the table reference
    table_ref = client.dataset(dataset_id).table(table_id)

    # Specify the Cloud Storage URI of the file
    uri = "gs://airflow-etl-bucket/currency_data.csv"

    # Specify the job configuration
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=0,  # Don't skip the header row in the CSV file
        source_format=bigquery.SourceFormat.CSV,  # Specify the source format
    )

    # Submit the job to load data into the table
    job = client.load_table_from_uri(uri, table_ref, job_config=job_config)

    # Wait for the job to complete
    job.result()


def load_data_to_final():

    # Replace 'your-project-id' with your actual project ID
    project_id = 'your-project-id'
    
    client = bigquery.Client(project=project_id)

    # Set up your dataset and table names
    dataset_id = 'currency'
    source_table_id = 'temp'
    destination_table_id = 'currency_table'

    # Construct the table references
    source_table_ref = client.dataset(dataset_id).table(source_table_id)
    destination_table_ref = client.dataset(dataset_id).table(destination_table_id)

    # Construct the SQL query to copy data from source to destination
    sql = f"""
        INSERT INTO `{project_id}.{dataset_id}.{destination_table_id}`
        SELECT *
        FROM `{project_id}.{dataset_id}.{source_table_id}`
    """

    # Run the query
    query_job = client.query(sql)

    # Wait for the query to finish
    query_job.result()


def delete_temp_table():

    # Replace 'your-project-id' with your actual project ID
    project_id = 'your-project-id'
    
    client = bigquery.Client(project=project_id)

    # Set up your dataset and table name
    dataset_id = 'currency'
    table_id = 'temp'

    # Construct the table reference
    table_ref = client.dataset(dataset_id).table(table_id)

    # Delete the table
    client.delete_table(table_ref)

