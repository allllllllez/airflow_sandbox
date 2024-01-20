from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
import os


with DAG(dag_id="dbt-installation-test", schedule_interval=None, catchup=False, start_date=days_ago(1)) as dag:
    cli_command = BashOperator(
        task_id="bash_command",
        # bash_command=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt --version"
        bash_command="/home/airflow/.local/bin/dbt --version"
    )
