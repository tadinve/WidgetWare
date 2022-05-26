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
    description="Update top revenue products data",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    extract_products = BashOperator(
        task_id="extract_products",
        bash_command=f'echo "extract_products"',
    )
    
    extract_order_details = BashOperator(
        task_id="extract_order_details",
        bash_command=f'echo "extract_order_details"',
    )

    merge_product_orders = BashOperator(
        task_id="merge_product_orders",
        bash_command=f'echo "merge_product_orders"',
    )
    
    aggregate_top_revenue_products = BashOperator(
        task_id="aggregate_top_revenue_products",
        bash_command=f'echo "aggregate_top_revenue_products"',
    )
    
    send_to_superset_dashboard = BashOperator(
        task_id="send_to_superset_dashboard",
        bash_command=f'echo "send_to_superset_dashboard"',
    )
    
    chain(
        begin,
        [extract_products,extract_order_details],
        merge_product_orders, 
        aggregate_top_revenue_products,
        send_to_superset_dashboard,
        end,
        )
