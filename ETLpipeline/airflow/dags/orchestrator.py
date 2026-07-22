from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys


def safe_main_callabel():
    from main import main
    return main()

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date' : datetime(2026, 7, 22),
    'catchup': False,
}

dag = DAG(
    dag_id = 'f1-api-orchestrator',
    default_arg = default_args,
    schedule = timedelta(weeks=1)
)


with dag:
    pass

