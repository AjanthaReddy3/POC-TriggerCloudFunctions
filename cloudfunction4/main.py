from google.cloud import bigquery

def query_avgtemp(request):
  client = bigquery.Client()
  query=  """
  SELECT location,average_temperature,latest_measurement 
  FROM `pg-us-e-app-588206.sample_data.table2` 
  WHERE average_temperature>=40 and latest_measurement>=current_date()-1900
  """
  query_job = client.query(query)
  print("The Query response is:")
  for row in query_job:
    print("location={}, avg_temp={}, latest_measurement={}".format(row[0],row[1],row[2]))
  return f'The Query ran successfully'
