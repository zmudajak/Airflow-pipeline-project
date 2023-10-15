#  importing libraries

import requests
from datetime import datetime
from datetime import timedelta
import pandas as pd
import gcsfs


def run_api_etl():
    # setting historical data to download currency exchange data
    today = datetime.now()
    historical_date = (today - timedelta(days=90)).strftime("%Y-%m-%d")

    # getting the data using requests.get function from Free Frankfurter Currency Exchange API endpoint
    url = f"http://api.frankfurter.app/{historical_date}.."
    data = requests.get(url=url)

    # converting data to pandas dataframe object and saving data in .csv format
    df = pd.DataFrame(data.json()['rates'])
    df.to_csv("gs://airflow-etl-bucket/currency_data.csv")
