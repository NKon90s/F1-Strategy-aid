from airflow import DAG
from datetime import datetime, timedelta
import sys
from airflow.providers.standard.operators.python import PythonOperator


sys.path.append('/opt/airflow/api_request')

def safe_create_db_callabel():
    from main import create_database
    return create_database()

def safe_data_to_db_callabel():
    from main import data_to_db
    return data_to_db()

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

