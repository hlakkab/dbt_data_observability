from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 2),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'is_paused_upon_creation': False
}

# Create the DAG with the specified schedule interval
dag = DAG('dag___freshnes_test', default_args=default_args, schedule_interval=timedelta(days=1))


run_model1 = BashOperator(
    task_id='run_model1',
    bash_command=r'/home/airflow/.local/bin/dbt run --models freshnes_test   --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/proj',
    dag=dag
)

dbt_data_quality_checks = BashOperator(
    task_id='dbt_data_quality_checks',
    bash_command=r'/home/airflow/.local/bin/dbt test --select "elementary_freshness_anomalies_freshnes_test_1_hour_created_at " --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/proj',
    dag=dag
)

run_model1 >> dbt_data_quality_checks

