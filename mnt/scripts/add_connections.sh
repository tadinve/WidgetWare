airflow connections delete 'forex_api'
airflow connections delete 'forex_path'
airflow connections delete 'hive_conn'
airflow connections delete 'spark_conn'

airflow connections add 'forex_api' --conn-type 'HTTP' --conn-host 'https://gist.github.com/' 

airflow connections add 'forex_path' --conn-type 'File' --conn-extra  '{"path":"/opt/airflow/dags/files/"}'

airflow connections add hive_conn \
  --conn-type 'Hive Server 2 Thrift' \
  --conn-host 'hive-server' \
  --conn-login 'hive' \
  --conn-password 'hive' \
  --conn-port '10000' 

airflow connections add spark_conn \
  --conn-type 'spark' \
  --conn-host 'spark://spark-master' \
  --conn-port '7077'