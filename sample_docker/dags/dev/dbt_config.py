#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a
virtual environment.
"""
from __future__ import annotations

import logging
import sys

from airflow.decorators import dag, task
from airflow.models.dagrun import DagRun
from airflow.models.param import Param
from airflow.models.taskinstance import TaskInstance
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pendulum import datetime

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable


@dag(
    dag_id="dbt_config",
    schedule=None,
    start_date=datetime(2023, 12, 7),
    catchup=False,
    tags=["example", "params"],
    params={
        "x": Param(5, type="integer", minimum=3),
        "my_int_param": 6
    },
)
def example_python_decorator():

    # prints <class 'str'> by default
    # prints <class 'int'> if render_template_as_native_obj=True
    py_operator = PythonOperator(
        task_id="py_operator",
        op_args=[
            "{{ params.my_int_param }}",
            "{{ params.x }}",
        ],
        python_callable=(
            lambda my_int_param, x: print(f'my_int_param: {my_int_param}, x: {x}')
        ),
    )

    @task(
        task_id="py_task",
    )
    def py_task_func(my_int_param, x):
        print(f'my_int_param: {my_int_param}, x: {x}')

    py_task = py_task_func("{{ params.my_int_param }}", "{{ params.x }}")  # これで DAG に渡した値を参照できる

    bash_task = BashOperator(
        task_id="bash_task",
        bash_command='echo \
            "Here is the message: my_int_param -> \'{{ dag_run.conf["my_int_param"] if dag_run else "" }}\', \
            x -> \'{{ dag_run.conf["x"] if dag_run else "" }}\'"',
    )

    bash_task >> py_operator >> py_task


example_python_decorator()
