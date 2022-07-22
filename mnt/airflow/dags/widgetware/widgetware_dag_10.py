from airflow import DAG
from datetime import timedelta, datetime

from airflow.operators.python_operator import PythonOperator
from airflow.settings import AIRFLOW_HOME
import update_top_rev_customers_data as dv1
import os

default_args = {
    'owner': 'neil_sonalkar',
    'depends_on_past': False,
    'start_date': datetime(2022, 2, 22),
    'email': ['neil_sonalkar@bmc.com'],
    'email_on_failure': False,
    'max_active_runs': 1,
    'email_on_retry': False,
    'provide_context':True
    #'retry_delay': timedelta(minutes=5)
}
dag = DAG(
    'update_top_revenue_products_data',
    start_date=datetime(2022, 6, 13),
    #max_active_runs=1,
    schedule_interval='@once',#'* * * * *',
    default_args=default_args,
    catchup=False
    )

extract_products = PythonOperator(task_id='extract_products',
                                   python_callable=dv1.extract_products,
                                   dag=dag)

extract_order_details = PythonOperator(task_id='extract_order_details',
                                   python_callable=dv1.extract_order_details,
                                   dag=dag)

merge_product_orders = PythonOperator(task_id='merge_product_orders',
                                   python_callable=dv1.merge_product_orders,
                                   dag=dag)

aggregate_top_revenue_products = PythonOperator(task_id='aggregate_top_revenue_products',
                                   python_callable=dv1.aggregate_top_revenue_products,
                                   dag=dag)

send_to_superset_dashboard = PythonOperator(task_id='send_to_superset_dashboard',
                                            python_callable=dv1.send_to_superset_dashboard,
                                            op_kwargs={'table':'top_revenue_products'},
                                            dag=dag)

extract_products >> extract_order_details >> merge_product_orders >> aggregate_top_revenue_products >> send_to_superset_dashboard
