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
    dag_id = 'f1-dbt-orchestrator',
    default_args = default_args,
    schedule = timedelta(weeks=1)
) 

with dag:
    task3 = DockerOperator(
        task_id = 'transform_data_task',
        image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command = 'run',
        working_dir = '/usr/app',
        Mounts = [
            Mount(source = 'D:/Coding projects/F1_strategy_aid/ETLpipeline/dbt/my_project',   #copy the absolute path of your 'my_project' folder
                  target = '/usr/app',
                  type = 'bind'),
            Mount(source = 'D:/Coding projects/F1_strategy_aid/ETLpipeline/dbt',     #copy the absolute path of your 'dbt' folder
                  target = '/root/.dbt/',
                  type = 'bind'),
        ],
        network_mode = 'my-network',
        docker_url = 'unix://var/run/docker.sock',
        auto_remove = 'success'
    )

