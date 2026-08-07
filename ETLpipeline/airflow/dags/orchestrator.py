from airflow import DAG
from datetime import datetime, timedelta
import sys
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

sys.path.append('/opt/airflow')

from api_request.main import create_database, data_to_db

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date' : datetime(2026, 8, 4),
    'catchup': False,
}
 
dag = DAG(
    dag_id = 'f1-api-dbt-orchestrator',
    default_args = default_args,
    schedule = timedelta(weeks=1)
)

with dag:
    
    task1 = PythonOperator(
        task_id = 'create_db_task',
        python_callable = create_database
    )
    
    task2 = PythonOperator(
            task_id = 'insert_data_task',
            python_callable = data_to_db
        )

    task3 = DockerOperator(
            task_id = 'transform_data_task',
            image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
            command = 'run',
            working_dir = '/usr/app',
            mounts = [
                Mount(source = 'D:/Coding projects/F1_strategy_aid/ETLpipeline/dbt/my_project',   #copy the absolute path of your 'my_project' folder
                      target = '/usr/app',
                      type = 'bind'),
                Mount(source = 'D:/Coding projects/F1_strategy_aid/ETLpipeline/dbt/profiles.yml',     #copy the absolute path of your 'dbt' folder
                      target = '/root/.dbt/profiles.yml',
                      type = 'bind'),
            ],
            network_mode = 'etlpipeline_my-network',
            mount_tmp_dir = False,
            docker_url = 'unix://var/run/docker.sock',
            auto_remove = 'success'
        )

    task1 >> task2 >> task3