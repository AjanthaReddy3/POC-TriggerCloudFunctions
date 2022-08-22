from google.cloud import bigquery
import os

def avgtemp_threshold_envvar(request):
  client = bigquery.Client()
  env_avg_temp=os.environ.get('avg_temp')
  
  query=  """
  SELECT location,average_temperature,latest_measurement 
  FROM `pg-us-e-app-588206.sample_data.table2` 
  WHERE average_temperature>=@average_temperature and latest_measurement>=current_date()-1900
  """
  job_config = bigquery.QueryJobConfig(
    query_parameters=[
      bigquery.ScalarQueryParameter("average_temperature", "INT64", env_avg_temp)
    ]
  ) 
  table_ref=client.dataset("sample_data").table("table3")
  job_config.destination=table_ref
  job_config.create_disposition = 'CREATE_IF_NEEDED'
  job_config.write_disposition = 'WRITE_TRUNCATE'
  print("env_avg_temp: {}".format(env_avg_temp))
  query_job = client.query(query, job_config=job_config)
  print("The Substituted Query: {}".format(query))
  #print("The Query response is: {}".format(query_job))
  results=query_job.result()
  if results.total_rows == 0:
    print ("There are no records with average Temperature > threshold.")
  else:
    for row in query_job:
      print(row)
    destination_uri="gs://poc-cloudfunctions/avgtemp_threshold.csv"
    dataset_ref=client.dataset("sample_data", project="pg-us-e-app-588206")
    table_ref=dataset_ref.table("table3")

    extract_job=client.extract_table(
      table_ref,
      destination_uri)
    extract_job.result()
  trigger_DAG()

  
  return f'The Query ran successfully!'
