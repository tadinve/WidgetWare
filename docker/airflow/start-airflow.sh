#!/usr/bin/env bash

# Create the user airflow in the HDFS
# hdfs dfs -mkdir -p    /user/airflow/
# hdfs dfs -chmod g+w   /user/airflow

# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME

# Export environement variables
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False
export PYTHONPATH='/opt/airflow:/opt/airflow/dags:/opt/airflow/plugins'

cd /dbt && dbt compile


# Initiliase the metadatabase
airflow db init

# Create User
airflow users create -e "admin@airflow.com" -f "airflow" -l "airflow" -p "airflow" -r "Admin" -u "airflow"

# Run the scheduler in background
airflow scheduler -D \
    -l $AIRFLOW_HOME/logs/scheduler/airflow-scheduler.log \
    --stderr $AIRFLOW_HOME/logs/scheduler/airflow-scheduler.stderr \
    --stdout $AIRFLOW_HOME/logs/scheduler/airflow-scheduler.stdout &> /dev/null &

# Add Postgres connection for DBT 
airflow connections add 'dbt_postgres' --conn-uri "postgres://${DBT_POSTGRES_USER}:${DBT_POSTGRES_PASSWORD}@${DBT_POSTGRES_HOST}:${POSTGRES_PORT}/${DBT_POSTGRES_DB}"

# Run the web sever in foreground (for docker logs)
exec airflow webserver