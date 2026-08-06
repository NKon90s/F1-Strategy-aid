from airflow import DAG
from datetime import datetime, timedelta
import sys
from airflow.providers.standard.operators.python import PythonOperator

sys.path.append('/opt/airflow')

from api_request.main import create_database, data_to_db

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date' : datetime(2026, 8, 4),
    'catchup': False,
}
 
dag = DAG(
    dag_id = 'f1-api-orchestrator',
    default_args = default_args,
    schedule = timedelta(weeks=1)
)

with dag:
    """
    task1 = PythonOperator(
        task_id = 'create_db_task',
        python_callable = create_database
    )
    """
    task2 = PythonOperator(
            task_id = 'insert_data_task',
            python_callable = data_to_db
        )

