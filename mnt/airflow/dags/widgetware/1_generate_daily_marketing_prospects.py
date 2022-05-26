import os 
from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
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
    description="Generate Daily Marketing Prospects",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    extract_mkt_web_data = BashOperator(
        task_id="extract_mkt_web_data",
        bash_command=f'echo "extract_mkt_web_data"',
    )
    
    extract_mkt_contacts = BashOperator(
        task_id="extract_mkt_contacts",
        bash_command=f'echo "extract_mkt_contacts"',
    )

    extract_dnb_data = BashOperator(
        task_id="extract_dnb_data",
        bash_command=f'echo "extract_dnb_data"',
    )
    
    merge_mktg_data = BashOperator(
        task_id="merge_mktg_data",
        bash_command=f'echo "merge_mktg_data"',
    )
    
    aggregate_prospects = BashOperator(
        task_id="aggregate_prospects",
        bash_command=f'echo "aggregate_prospects"',
    )

    push_prospects_to_big_query = BashOperator(
        task_id="push_prospects_to_big_query",
        bash_command=f'echo "push_prospects_to_big_query"',
    )

    publish_top_prospects_to_google_studio = BashOperator(
        task_id="publish_top_prospects_to_google_studio",
        bash_command=f'echo "publish_top_prospects_to_google_studio"',
    )
    
    chain(
        begin,
        [extract_mkt_web_data, extract_mkt_contacts, extract_dnb_data],
        merge_mktg_data,
        aggregate_prospects, 
        push_prospects_to_big_query, 
        publish_top_prospects_to_google_studio,
        end,
        )
