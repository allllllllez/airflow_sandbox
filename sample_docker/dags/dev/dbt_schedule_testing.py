from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from pendulum import datetime

with DAG(
    dag_id="dbt_schedule_testing",
    schedule_interval='* */1 * * *',
    catchup=False,
    start_date=datetime(
        2023, 12, 8,
        tz="Asia/Tokyo")
) as dag:
    cli_command = BashOperator(
        task_id="bash_command",
        # bash_command=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt --version"
        bash_command="/home/airflow/.local/bin/dbt --version"
    )
