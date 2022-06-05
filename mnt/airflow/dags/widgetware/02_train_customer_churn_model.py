import os 
from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.models.baseoperator import chain

DAG_ID = os.path.basename(__file__).replace(".py", "")

DEFAULT_ARGS = {
    "owner": "pjasthi@bmc.com",
    "depends_on_past": False,
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    dag_id=DAG_ID,
    description="Train Customer Churn ML Model",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    extract_product_active_use = BashOperator(
        task_id="extract_product_active_use",
        bash_command=f'echo "extract_product_active_use"',
    )
    
    extract_product_survey_data = BashOperator(
        task_id="extract_product_survey_data",
        bash_command=f'echo "extract_product_survey_data"',
    )

    extract_product_renewals = BashOperator(
        task_id="extract_product_renewals",
        bash_command=f'echo "extract_product_renewals"',
    )
    
    merge_product_data = BashOperator(
        task_id="merge_product_data",
        bash_command=f'echo "merge_product_data"',
    )
    
    aggregate_product_data = BashOperator(
        task_id="aggregate_product_data",
        bash_command=f'echo "aggregate_product_data"',
    )

    push_churn_features_to_snowflake = BashOperator(
        task_id="push_churn_features_to_snowflake",
        bash_command=f'echo "push_churn_features_to_snowflake"',
    )

    train_churn_model_on_databricks = BashOperator(
        task_id="train_churn_model_on_databricks",
        bash_command=f'echo "train_churn_model_on_databricks"',
    )
    
    chain(
        begin,
        [extract_product_active_use, extract_product_survey_data, extract_product_renewals],
        merge_product_data, 
        aggregate_product_data, 
        push_churn_features_to_snowflake, 
        train_churn_model_on_databricks,
        end,
        )
