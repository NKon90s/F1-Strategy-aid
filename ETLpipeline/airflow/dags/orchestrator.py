from airflow import DAG
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/api_request')

def safe_main_callabel():
    pass

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

