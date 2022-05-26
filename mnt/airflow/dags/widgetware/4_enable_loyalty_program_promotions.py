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
    description="Enable promotions to loyalty program customers",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    get_customers_data = BashOperator(
        task_id="get_customers_data",
        bash_command=f'echo "get_customers_data"',
    )
    
    get_orders_history = BashOperator(
        task_id="get_orders_history",
        bash_command=f'echo "get_orders_history"',
    )

    process_customer_order_history = BashOperator(
        task_id="process_customer_order_history",
        bash_command=f'echo "process_customer_order_history"',
    )
    
    identify_loyalty_promotion_customers = BashOperator(
        task_id="identify_loyalty_promotion_customers",
        bash_command=f'echo "identify_loyalty_promotion_customers"',
    )
    
    send_loyalty_list_to_hubspot = BashOperator(
        task_id="send_loyalty_list_to_hubspot",
        bash_command=f'echo "send_loyalty_list_to_hubspot"',
    )
    
    chain(
        begin,
        [get_customers_data, get_orders_history],
        process_customer_order_history, 
        identify_loyalty_promotion_customers,
        send_loyalty_list_to_hubspot,
        end,
        )
