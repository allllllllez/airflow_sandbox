from __future__ import annotations

import logging
import os
from pathlib import Path

from airflow.decorators import dag
from airflow.models.param import Param
from airflow.operators.empty import EmptyOperator
from cosmos import DbtTaskGroup, ProfileConfig, ProjectConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from pendulum import datetime

log = logging.getLogger(__name__)

profile_config = ProfileConfig( 
    profile_name="default",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="airflow_id",
        profile_args={"schema": "public"},
    ),
)

DEFAULT_DBT_ROOT_PATH = Path(__file__).parent / "dbt" 
DBT_ROOT_PATH = Path(os.getenv("DBT_ROOT_PATH", DEFAULT_DBT_ROOT_PATH))


@dag(
    schedule=None,
    start_date=datetime(2023, 12, 7),
    catchup=False,
    tags=["example", "params"],
    params={
        "x": Param(5, type="integer", minimum=3),
        "my_int_param": 6
    },
    dag_id="dbt_config_cosmos",
    default_args={"retries": 2},
)
def cosmos_profile_mapping() -> None:
    pre_dbt = EmptyOperator(task_id="pre_dbt")

    project = DbtTaskGroup(
        # dbt/cosmos-specific parameters
        project_config=ProjectConfig(
            DBT_ROOT_PATH / "project",
        ),
        profile_config=profile_config,
    )

    post_dbt = EmptyOperator(task_id="post_dbt")

    pre_dbt >> project >> post_dbt


cosmos_profile_mapping()
