import sys
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date' : datetime(2026, 7, 26),
    'catchup': False,
}

dag = DAG(
    dag_id = 'f1-api-orchestrator',
    default_args = default_args,
    schedule = timedelta(weeks=1)
)