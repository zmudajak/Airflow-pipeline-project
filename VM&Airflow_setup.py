# Update the files and install libraries
sudo apt-get update
sudo apt install python3-pip
sudo pip install apache-airflow
sudo pip install pandas
sudo pip install gcsfs

#browse to airflow folder
cd airflow
sudo nano airflow.cfg #edit the dag folder name and ctrl+x & save

#create the files and copy their content inside & save
cd [your dag folder name]
sudo nano airflow_etl.py
sudo nano api_etl_dag.py

# turn on airflow standalone
airflow standalone