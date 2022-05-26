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
    description="Generate biweekly employee payroll stubs",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    get_employees_salary = BashOperator(
        task_id="get_employees_salary",
        bash_command=f'echo "get_employees_salary"',
    )
    
    get_employees_deductions = BashOperator(
        task_id="get_employees_deductions",
        bash_command=f'echo "get_employees_deductions"',
    )

    calculate_employees_pay_stub = BashOperator(
        task_id="calculate_employees_pay_stub",
        bash_command=f'echo "calculate_employees_pay_stub"',
    )
    
    generate_pay_stub_file = BashOperator(
        task_id="generate_pay_stub_file",
        bash_command=f'echo "generate_pay_stub_file"',
    )
    
    email_paystub_links = BashOperator(
        task_id="email_paystub_links",
        bash_command=f'echo "email_paystub_links"',
    )
    
    chain(
        begin,
        [get_employees_salary, get_employees_deductions],
        calculate_employees_pay_stub, 
        generate_pay_stub_file,
        email_paystub_links,
        end,
        )
