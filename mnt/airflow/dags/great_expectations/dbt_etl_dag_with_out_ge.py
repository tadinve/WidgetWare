from datetime import datetime
import airflow
from airflow import AirflowException
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
import os
from airflow.utils.log.logging_mixin import LoggingMixin


# from airflow_dbt.operators.dbt_operator import (
#     DbtSeedOperator,
#     DbtRunOperator
# )
# from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

DBT_PROJECT_DIR = "/dbt"
DBT_TARGET_DIR = "/dbt/target"
DBT_DOCS_DIR = "/include/dbt_docs"

# Global variables that are set using environment varaiables
GE_DATA_PATH = '/dbt/sample_data'
GE_ROOT_PATH = '/great_expectations'
GE_TARGET_DIR = '/great_expectations/uncommitted/data_docs'
GE_DOCS_DIR = "/include/great_expectations_docs"

class DbtOperator(BashOperator):
    # ui_color = "#ff0000"
    # ui_fgcolor = "#000000"
    ui_color = "#E0D18F"
    ui_fgcolor = "#000000"
    
def load_to_production_db(ts, **kwargs):
    """
    This is just a stub for an optional Python task that loads the output of the dbt pipeline
    to a production database or data warehouse for further consumption
    """
    LoggingMixin().log.info('Loading analytical_output output to production database.')
    LoggingMixin().log.info('Done.')
    
    
DAG_ID = os.path.basename(__file__).replace(".py", "")

with DAG(
    DAG_ID,
    start_date=datetime(2020, 12, 23),
    description="A sample Airflow DAG to invoke great expectations",
    schedule_interval=None,
    catchup=False,
    default_args={
        "env": {
            "DBT_USER": "{{ conn.dbt_postgres.login }}",
            "DBT_ENV_SECRET_PASSWORD": "{{ conn.dbt_postgres.password }}",
            "DBT_HOST": "{{ conn.dbt_postgres.host }}",
            "DBT_SCHEMA": "{{ conn.dbt_postgres.schema }}",
            "DBT_PORT": "{{ conn.dbt_postgres.port }}",
        }
    },
) as dag:
    
    
    # start_task = BashOperator(
    #     task_id='start_task',
    #     bash_command="echo 'Start Task' "
    # )
    
    load_files_into_db = DbtOperator(
        task_id="load_files_into_db",
        bash_command=f"dbt seed --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    transform_data_in_db = DbtOperator(
        task_id="transform_data_in_db",
        bash_command=f"dbt run --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    # dbt_test = BashOperator(
    #     task_id="dbt_test",
    #     bash_command=f"dbt test --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    # )
    
    generate_dbt_docs = DbtOperator(
        task_id='generate_dbt_docs',
        bash_command=f'dbt docs generate --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}'
    )
    
    copy_dbt_docs = DbtOperator(
        task_id='copy_dbt_docs',
        bash_command=f'mkdir {DBT_DOCS_DIR}; cp -r {DBT_TARGET_DIR} {DBT_DOCS_DIR}'
    )
    
    
    load_to_prod = PythonOperator(
        task_id='load_to_prod',
        python_callable=load_to_production_db
    )



load_files_into_db >> transform_data_in_db >> generate_dbt_docs >> copy_dbt_docs >> load_to_prod


