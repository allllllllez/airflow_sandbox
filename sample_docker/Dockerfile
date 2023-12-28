FROM apache/airflow:2.6.3-python3.8

ENV AIRFLOW_HOME=/opt/airflow
# ENV DBT_VENV_PATH="${AIRFLOW_HOME}/dbt_venv"
ENV PIP_USER=false

ADD requirements.txt .

# RUN python -m venv "${DBT_VENV_PATH}" && \
    # ${DBT_VENV_PATH}/bin/pip install --no-cache-dir -r requirements.txt
RUN python -m pip install --user --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

ENV PIP_USER=true
