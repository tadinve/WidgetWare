from datetime import datetime
import airflow
from airflow import AirflowException
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
import os
from airflow.utils.log.logging_mixin import LoggingMixin
import great_expectations as ge
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.data_context import DataContext
from great_expectations.core.batch import BatchRequest
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from great_expectations.cli.datasource import check_if_datasource_name_exists

from plugins.create_ge_datasources import GE_Data_Sources
from plugins.create_ge_suites import GE_Suites
from plugins.create_ge_checkpoints import GE_Checkpoints
# from airflow_dbt.operators.dbt_operator import (
#     DbtSeedOperator,
#     DbtRunOperator
# )
# from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

DBT_PROJECT_DIR = "/dbt"
DBT_TARGET_DIR = "/dbt/target"
DBT_DOCS_DIR = "/include/dbt_docs"

# Global variables that are set using environment varaiables
GE_DATA_PATH = '../dbt/sample_data'
GE_ROOT_PATH = '/great_expectations'
GE_TARGET_DIR = '/great_expectations/uncommitted/data_docs'
GE_DOCS_DIR = "/include/great_expectations_docs"


class DbtOperator(BashOperator):
    # ui_color = "#ff0000"
    # ui_fgcolor = "#000000"
    ui_color = "#E0D18F"
    ui_fgcolor = "#000000"

class GreatExpectationsOperator(PythonOperator):
    ui_color = "#8FCCE0"
    ui_fgcolor = "#000000"    

class GreatExpectationsCommandOperator(BashOperator):
    ui_color = "#8FCCE0"
    ui_fgcolor = "#000000"    
    
def load_to_production_db(ts, **kwargs):
    """
    This is just a stub for an optional Python task that loads the output of the dbt pipeline
    to a production database or data warehouse for further consumption
    """
    LoggingMixin().log.info('Loading analytical_output output to production database.')
    LoggingMixin().log.info('Done.')

def prepare_ge_sources_dict():
    sources_dict = {}
    for datasource_name in ge.get_context().list_datasources():
        data_asset_names_dict = ge.get_context().get_available_data_asset_names(datasource_name['name'])
        sources_dict[datasource_name['name']] = data_asset_names_dict[datasource_name['name']]['default_inferred_data_connector_name'] 
    return sources_dict

def validate_data(check_point_name):
    
    data_context: DataContext = DataContext(
        context_root_dir=GE_ROOT_PATH
    )

    result: CheckpointResult = data_context.run_checkpoint(
        checkpoint_name=check_point_name,
        batch_request=None,
        run_name=None,
    )
    
    if not result["success"]:
        LoggingMixin().log.error('Great Expectations validation failed! for Checkpoint: {}'.format(check_point_name))
        raise AirflowException("Validation of the source data is not successful ")
    else:
        LoggingMixin().log.info('Great Expectations validation success! for Checkpoint: {}'.format(check_point_name))

def process_ge_generators(data_source, data_dir=None, db_args=None):
    
    if not check_if_datasource_name_exists(ge.get_context(), data_source):
        GE_Data_Sources.create_data_source(datasource=data_source, data_dir=data_dir, args_json=db_args)
    else:
        LoggingMixin().log.info('Skipping the creation of data source in ge')
    
    sources_dict = prepare_ge_sources_dict()    
    
    LoggingMixin().log.info('sources_dict::'.format(sources_dict))
        
    # create expectations for data assets
    for data_asset in sources_dict[data_source]:
        GE_Suites.create_suite_files(datasource_name=data_source, data_asset_name=data_asset)    
    
    # create checkpoint for data assets
    check_point_config = GE_Checkpoints.create_check_point_config(sources_dict)      
    GE_Checkpoints.create_check_points(check_point_config)

def validate_source_data():
    # Check if the datasource exists 
    process_ge_generators('input_files', data_dir=GE_DATA_PATH)
    validate_data('check_csv_files')

def validate_raw_data():
    process_ge_generators('postgres_datasource', db_args=args_json)
    validate_data('check_raw_tables')
    
def validate_stage_data():
    process_ge_generators('postgres_datasource', db_args=args_json)
    validate_data('check_stg_tables')
    
def validate_transformed_data():
    validate_data('check_transform_tables')  
        
    
DAG_ID = os.path.basename(__file__).replace(".py", "")

args_json = {
    'host': 'postgres-dbt',
    'port': 5432,
    'username':  'dbtuser',
    'password': 'pssd',
    'database': 'dbtdb',
    'schema_name': 'dbt'
}


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
    
    
    task_validate_source_data = GreatExpectationsOperator(
        task_id='task_validate_source_data',
        python_callable=validate_source_data
    )
    
    task_validate_raw_data = GreatExpectationsOperator(
        task_id='task_validate_raw_data',
        python_callable=validate_raw_data
    )
    
    task_validate_stage_data = GreatExpectationsOperator(
        task_id='task_validate_stage_data',
        python_callable=validate_stage_data
    )
    
    task_validate_transformed_data = GreatExpectationsOperator(
        task_id='task_validate_transformed_data',
        python_callable=validate_transformed_data
    )
    
    load_files_into_db = DbtOperator(
        task_id="load_files_into_db",
        bash_command=f"dbt seed --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    transform_data_in_db = DbtOperator(
        task_id="transform_data_in_db",
        bash_command=f"dbt run --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    generate_dbt_docs = DbtOperator(
        task_id='generate_dbt_docs',
        bash_command=f'dbt docs generate --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}'
    )
    
    copy_dbt_docs = DbtOperator(
        task_id='copy_dbt_docs',
        bash_command=f'mkdir {DBT_DOCS_DIR}; cp -r {DBT_TARGET_DIR} {DBT_DOCS_DIR}'
    )
    
    generate_ge_docs = GreatExpectationsCommandOperator(
        task_id='generate_ge_docs',
        bash_command=f'great_expectations -y docs build'
    )
    
    copy_ge_docs = GreatExpectationsCommandOperator(
        task_id='copy_ge_docs',
        bash_command=f'mkdir {GE_DOCS_DIR}; cp -r {GE_TARGET_DIR} {GE_DOCS_DIR}'
    )
    load_to_prod = PythonOperator(
        task_id='load_to_prod',
        python_callable=load_to_production_db
    )


task_validate_source_data >> load_files_into_db >> task_validate_raw_data >> transform_data_in_db
transform_data_in_db >> task_validate_stage_data >> task_validate_transformed_data >> [generate_dbt_docs, generate_ge_docs]
generate_dbt_docs >> copy_dbt_docs
generate_ge_docs >> copy_ge_docs
[copy_dbt_docs, copy_ge_docs] >> load_to_prod


