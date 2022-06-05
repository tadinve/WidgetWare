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
    description="Process daily insurance claims",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    load_claims_data = BashOperator(
        task_id="load_claims_data",
        bash_command=f'echo "load_claims_data"',
    )
    
    transcribe_documents = BashOperator(
        task_id="transcribe_documents",
        bash_command=f'echo "transcribe_documents"',
    )

    submit_to_claim_audit_model = BashOperator(
        task_id="submit_to_claim_audit_model",
        bash_command=f'echo "submit_to_claim_audit_model"',
    )
    
    initiate_approval_process = BashOperator(
        task_id="initiate_approval_process",
        bash_command=f'echo "initiate_approval_process"',
    )
    
    chain(
        begin,
        load_claims_data,
        transcribe_documents, 
        submit_to_claim_audit_model,
        initiate_approval_process,
        end,
        )
