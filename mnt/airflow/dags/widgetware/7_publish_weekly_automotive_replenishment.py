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
    description="Publish weekly automotive parts replenishment",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    get_sales_history_data = BashOperator(
        task_id="get_sales_history_data",
        bash_command=f'echo "get_sales_history_data"',
    )
    
    get_stock_list_data = BashOperator(
        task_id="get_stock_list_data",
        bash_command=f'echo "get_stock_list_data"',
    )

    combine_parts_stock = BashOperator(
        task_id="combine_parts_stock",
        bash_command=f'echo "combine_parts_stock"',
    )
    
    generate_inventory_report = BashOperator(
        task_id="generate_inventory_report",
        bash_command=f'echo "generate_inventory_report"',
    )

    
    chain(
        begin,
        [get_sales_history_data, get_stock_list_data],
        combine_parts_stock, 
        generate_inventory_report,
        end,
        )
