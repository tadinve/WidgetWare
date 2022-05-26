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
    description="Pass training data to Anomaly Detection Model",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["widgetware"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")
    
    import_rad_images = BashOperator(
        task_id="import_rad_images",
        bash_command=f'echo "import_rad_images"',
    )
    
    import_path_images = BashOperator(
        task_id="import_path_images",
        bash_command=f'echo "import_path_images"',
    )

    import_cardio_images = BashOperator(
        task_id="import_cardio_images",
        bash_command=f'echo "import_cardio_images"',
    )
    
    transfer_to_gcp = BashOperator(
        task_id="transfer_to_gcp",
        bash_command=f'echo "transfer_to_gcp"',
    )
    
    train_model_bigquery_ml = BashOperator(
        task_id="train_model_bigquery_ml",
        bash_command=f'echo "train_model_bigquery_ml"',
    )

    
    chain(
        begin,
        [import_rad_images, import_path_images, import_cardio_images],
        transfer_to_gcp, 
        train_model_bigquery_ml,
        end,
        )
