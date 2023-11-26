#code below is used to create main table in BigQuery
gcloud auth login #if entered by cloud shell button should be by default
gcloud config set project YOUR_PROJECT_ID #if not currently in your project
#make dataset
bq mk currency
#make table
bq mk \
  --table \
  --schema "date:date, USD:float" \
  currency.currency_table