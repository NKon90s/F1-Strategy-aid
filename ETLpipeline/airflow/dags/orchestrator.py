from airflow import DAG
from datetime import datetime, timedelta
import sys
from airflow.providers.standard.operators.python import PythonOperator
from api_request.main import create_database, data_to_db

sys.path.append('/opt/airflow/api_request')

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
    task1 = PythonOperator(
        task_id = 'create_db_task',
        python_callable = create_database
    )


