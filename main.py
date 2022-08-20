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
  query_job = client.query(query, job_config=job_config)
  print("The Query response is:")
  for row in query_job:
    print("location={}, avg_temp={}, latest_measurement={}".format(row[0],row[1],row[2]))
  return f'The Query ran successfully!'
