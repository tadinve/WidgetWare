from email import message
from email.mime import application
from re import sub
from socket import timeout
from tabnanny import verbose
from termios import TABDLY
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.email import EmailOperator

from datetime import datetime,timedelta

import requests
import csv
import json


default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "pjasthi@bmc.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

# Download forex rates according to the currencies we want to watch
# described in the file forex_currencies.csv
def download_rates():
    BASE_URL = "https://gist.githubusercontent.com/marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b/raw/"
    ENDPOINTS = {
        'USD': 'api_forex_exchange_usd.json',
        'EUR': 'api_forex_exchange_eur.json'
    }
    with open('/opt/airflow/dags/files/forex_currencies.csv') as forex_currencies:
        reader = csv.DictReader(forex_currencies, delimiter=';')
        for idx, row in enumerate(reader):
            base = row['base']
            with_pairs = row['with_pairs'].split(' ')
            indata = requests.get(f"{BASE_URL}{ENDPOINTS[base]}").json()
            outdata = {'base': base, 'rates': {}, 'last_update': indata['date']}
            for pair in with_pairs:
                outdata['rates'][pair] = indata['rates'][pair]
            with open('/opt/airflow/dags/files/forex_rates.json', 'a') as outfile:
                json.dump(outdata, outfile)
                outfile.write('\n')

with DAG("forex_data_pipeline",start_date=datetime(2021,1,1), 
        schedule_interval="@daily",default_args=default_args,
        catchup=False) as dag:

    reset_data = BashOperator(
        task_id = "reset_data",
        bash_command="/opt/airflow/dags/scripts/reset_data.sh "
    )

    add_conns = BashOperator(
        task_id = "add_conns",
        bash_command="/opt/airflow/dags/scripts/add_connections.sh "
    )

    is_forex_rates_available = HttpSensor(
        task_id = "is_forex_rates_available",
        http_conn_id="forex_api",
        endpoint="marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b",
        response_check=lambda response: "rates" in response.text, 
        poke_interval = 5,
        timeout = 20
    )

    is_forex_curr_available = FileSensor(
        task_id = "is_forex_curr_available",
        fs_conn_id = "forex_path",
        filepath = "forex_currencies.csv",
        poke_interval = 5,
        timeout = 20
    )
    
    download_forex_file = PythonOperator(
        task_id = "download_forex_file",
        python_callable=download_rates
    )

    saving_rates = BashOperator(
        task_id = "saving_rates",
        bash_command="""
            hdfs dfs -mkdir -p /forex && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex
        """
    )
    
    drop_forex_rates_table = HiveOperator(
        task_id="drop_forex_rates_table",
        hive_cli_conn_id="hive_conn",
        hql="""
            DROP TABLE IF EXISTS forex_rates
        """
    )


    creating_forex_rates_table = HiveOperator(
        task_id="creating_forex_rates_table",
        hive_cli_conn_id="hive_conn",
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
                )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """
    )

    
    forex_processing = SparkSubmitOperator(
        task_id = "forex_processing",
        application="/opt/airflow/dags/scripts/forex_processing.py",
        conn_id = "spark_conn",
        verbose=False
    )

    send_email = EmailOperator(
        task_id = "send_email",
        subject = "Forex Pipleline",
        to='pjasthi@bmc.com', 
        html_content="<h3> Processed successfully</>"
    )


    reset_data >> add_conns >> drop_forex_rates_table >> is_forex_rates_available 
    is_forex_rates_available >> is_forex_curr_available >> download_forex_file
    download_forex_file >> saving_rates >> creating_forex_rates_table 
    creating_forex_rates_table >> forex_processing >> send_email

