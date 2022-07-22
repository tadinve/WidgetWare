from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
import update_top_rev_customers_data as dv1

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
    'update_top_revenue_customers_data',
    start_date=datetime(2022, 6, 13),
    #max_active_runs=1,
    schedule_interval='@once',#'* * * * *',
    default_args=default_args,
    catchup=False
    )

extract_customers = PythonOperator(task_id='extract_customers',
                                   python_callable=dv1.extract_customers,
                                   dag=dag)

extract_order_details = PythonOperator(task_id='extract_order_details',
                                   python_callable=dv1.extract_order_details,
                                   dag=dag)

merge_customers_orders = PythonOperator(task_id='merge_customers_orders',
                                   python_callable=dv1.merge_customers_orders,
                                   dag=dag)

aggregate_top_revenue_customers = PythonOperator(task_id='aggregate_top_revenue_customers',
                                   python_callable=dv1.aggregate_top_revenue_customers,
                                   dag=dag)

send_to_superset_dashboard = PythonOperator(task_id='send_to_superset_dashboard',
                                            python_callable=dv1.send_to_superset_dashboard,
                                            op_kwargs={'table':'top_revenue_customers'},
                                            dag=dag)

extract_customers >> extract_order_details >> merge_customers_orders >> aggregate_top_revenue_customers >> send_to_superset_dashboard
