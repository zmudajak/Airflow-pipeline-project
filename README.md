
# Airflow ETL pipeline project

The purpose of this project is to build ETL pipeline using Apache Airflow in Google Cloud Platform environment to provide data for further analysis using BigQuery/LookerStudios. It does this by getting data from [Frankfurter](https://www.frankfurter.app/) a free currency exchange API.
The pipeline is built to connect to API endpoint using python script (filename.py) and getting currency exchange data from last 90 days which is then migrated to GCP Storage by Apache Airflow run on Google Cloud's Virtual Machine.
