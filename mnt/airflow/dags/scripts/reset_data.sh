rm -rf /opt/airflow/dags/files/*.json
hdfs dfs -test -d /forex
if [ $? == 0 ]
then
    echo "forex directory exists and hence deleting it"
    hdfs dfs -rm -r /forex
    hdfs dfs -rm -r /user/hive/warehouse/forex_rates
else
    echo "dir does not exists..skipping"
fi
