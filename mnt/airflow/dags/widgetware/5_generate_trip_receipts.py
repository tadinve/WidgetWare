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
    description="Generate receipts for trips",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    get_trip_details = BashOperator(
        task_id="get_trip_details",
        bash_command=f'echo "get_trip_details"',
    )
    
    get_payment_orders = BashOperator(
        task_id="get_payment_orders",
        bash_command=f'echo "get_payment_orders"',
    )

    process_payments_with_gateway = BashOperator(
        task_id="process_payments_with_gateway",
        bash_command=f'echo "process_payments_with_gateway"',
    )
    
    generate_invoice_statements = BashOperator(
        task_id="generate_invoice_statements",
        bash_command=f'echo "generate_invoice_statements"',
    )
    
    email_receipts = BashOperator(
        task_id="email_receipts",
        bash_command=f'echo "email_receipts"',
    )
    
    chain(
        begin,
        [get_trip_details, get_payment_orders],
        process_payments_with_gateway, 
        generate_invoice_statements,
        email_receipts,
        end,
        )
