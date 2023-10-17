
![](airflow-etl-screenshots/pipeline_picture.jpg)

# Airflow ETL pipeline project

Special thanks to [DarshilParmar](https://www.youtube.com/@DarshilParmar) for his guide and inspiration to re-create this project in GCP!

## Purpose

The purpose of this project is to build ETL pipeline using Apache Airflow in Google Cloud Platform environment to provide data for further analysis using BigQuery/LookerStudios. It does this by getting data from [Frankfurter](https://www.frankfurter.app/) a free currency exchange API.
The pipeline is built to connect to API endpoint using python script (filename.py) and getting currency exchange data from last 90 days which is then migrated to GCP Storage by Apache Airflow run on Google Cloud's Virtual Machine.

## Technologies used

Python, REST API, Airflow, GCP

## Step-by-step guide:

### 1. Make sure you have Google Cloud Platform account

To create free account you can go to [Google Cloud Page](https://cloud.google.com/). Create your project and continue from here.

### 2. Create Storage Bucket

Use google cloud console > Cloud storage > Buckets and create new bucket named 'airflow-etl-bucket'.

### 3. Create Virtual Machine

Google cloud console > Compute Engine > Virtual Machines. 

You can choose whichever VM you want but this project was made on E2-standard-4.

**Important thing is to [enable HTTP/HTTPS traffic](airflow-etl-screenshots/GCP-VM-firewalls.JPG).**<br>
**2nd important thing is setting access scopes to [allow access to all cloud API](airflow-etl-screenshots/GCP-access-scopes.JPG).**

### 4. Set up firewall rule to allow SSH access from your PC.

Find out your IP at [WhatIsMyIP](https://www.whatismyip.com/) - you are interested in IPv4.

From main VM screen click on 'Set up firewall rule' > Create new rule.<br>
From there the most important thing is to [provide your IP (source IPv4 ranges) and select TCP port](airflow-etl-screenshots/GCP-firewall-rule.JPG). In example is 8080 which is local port. Remember you will later connect to this port.

### 5. Set up your VM and Configure Airflow

Connect with VM by [SSH button](airflow-etl-screenshots/GCP-VM-externalIPSSH.JPG) in GCP interface.<br>
Update the files and get necessary libraries (code here).<br>
Start airflow server (do not close this window). Airflow server password and login are in the terminal window after airflow standalone is started.<br>
Open another terminal window.<br>
Browse to your airflow folder and edit [airflow.cfg file to change dags folder name](airflow-etl-screenshots/airflow-cfg.JPG) (in example 'api_dag'). Save changes.<br>
Make directory same as you named dags folder (in example 'api_dag').<br>
Change directory to your dags folder. Make files 'api_etl_dag.py' and 'airflow_etl.py' and copy their contents from repository. Save changes.<br>
Restart airflow server. (ctrl+c > airflow standalone)

### 6. Run pipeline

Log in to your airflow server via VM [external IP](airflow-etl-screenshots/GCP-VM-externalIPSSH.JPG) in your browser adding ':8080' as local port (for example: 00.000.0.000:8080). <br>
Your DAG should be visible. Click DAG > Graph > [Run]((airflow-etl-screenshots/airflow-dag-window.JPG)).<br>
If everything is successfull you should see the file in your GCP bucket.<br>
Congratulations! Remember to shut down your VM and delete data in your storage bucket to save $$!
