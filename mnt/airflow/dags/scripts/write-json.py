from asyncore import read
import json
json_file = "tasks_data.json"
def read_file(fn):
    f = open(fn,"r")
    s = f.read()
    tasks = json.loads(s)
    return tasks

def write_json():
  td = {
    "tasks": [
      {
        "class_ref": {
          "class_name": "BashOperator",
          "module_path": "airflow.operators.bash"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "drop_forex_rates_table"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "add_conns",
        "template_fields": [
          "bash_command",
          "env"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#f0ede4",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "HiveOperator",
          "module_path": "airflow.providers.apache.hive.operators.hive"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "forex_processing"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "creating_forex_rates_table",
        "template_fields": [
          "hql",
          "schema",
          "hive_cli_conn_id",
          "mapred_queue",
          "hiveconfs",
          "mapred_job_name",
          "mapred_queue_priority"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#f0e4ec",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "PythonOperator",
          "module_path": "airflow.operators.python"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "saving_rates"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "download_forex_file",
        "template_fields": [
          "templates_dict",
          "op_args",
          "op_kwargs"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#ffefeb",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "HiveOperator",
          "module_path": "airflow.providers.apache.hive.operators.hive"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "is_forex_rates_available"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "drop_forex_rates_table",
        "template_fields": [
          "hql",
          "schema",
          "hive_cli_conn_id",
          "mapred_queue",
          "hiveconfs",
          "mapred_job_name",
          "mapred_queue_priority"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#f0e4ec",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "SparkSubmitOperator",
          "module_path": "airflow.providers.apache.spark.operators.spark_submit"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "send_email"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "forex_processing",
        "template_fields": [
          "_application",
          "_conf",
          "_files",
          "_py_files",
          "_jars",
          "_driver_class_path",
          "_packages",
          "_exclude_packages",
          "_keytab",
          "_principal",
          "_proxy_user",
          "_name",
          "_application_args",
          "_env_vars"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#FF9933",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "FileSensor",
          "module_path": "airflow.sensors.filesystem"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "download_forex_file"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "is_forex_curr_available",
        "template_fields": [
          "filepath"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#91818a",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "HttpSensor",
          "module_path": "airflow.providers.http.sensors.http"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "is_forex_curr_available"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "is_forex_rates_available",
        "template_fields": [
          "endpoint",
          "request_params",
          "headers"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#e6f1f2",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "BashOperator",
          "module_path": "airflow.operators.bash"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "add_conns"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "reset_data",
        "template_fields": [
          "bash_command",
          "env"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#f0ede4",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "BashOperator",
          "module_path": "airflow.operators.bash"
        },
        "depends_on_past": False,
        "downstream_task_ids": [
          "creating_forex_rates_table"
        ],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "saving_rates",
        "template_fields": [
          "bash_command",
          "env"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#f0ede4",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      },
      {
        "class_ref": {
          "class_name": "EmailOperator",
          "module_path": "airflow.operators.email"
        },
        "depends_on_past": False,
        "downstream_task_ids": [],
        "end_date": None,
        "execution_timeout": None,
        "extra_links": [],
        "owner": "airflow",
        "params": {},
        "pool": "default_pool",
        "pool_slots": 1.0,
        "priority_weight": 1.0,
        "queue": "default",
        "retries": 1.0,
        "retry_delay": {
          "__type": "TimeDelta",
          "days": 0,
          "microseconds": 0,
          "seconds": 300
        },
        "retry_exponential_backoff": False,
        "start_date": "2021-01-01T00:00:00+00:00",
        "task_id": "send_email",
        "template_fields": [
          "to",
          "subject",
          "html_content",
          "files"
        ],
        "trigger_rule": "all_success",
        "ui_color": "#e6faf9",
        "ui_fgcolor": "#000",
        "wait_for_downstream": False,
        "weight_rule": "downstream"
      }
    ],
    "total_entries": 10
  }
  #print(td)
  with open(json_file, 'w') as outfile:
      json.dump(td, outfile)

write_json()
td2 = read_file(json_file)
print(type(td2))