from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG with the specified schedule interval
dag = DAG('dag___dbt', default_args=default_args, schedule_interval=timedelta(days=1))


# Define dbt tasks using BashOperator
run_model1 = BashOperator(
    task_id='run_model1',
    bash_command=r'/home/airflow/.local/bin/dbt run --models my_first_dbt_model my_second_dbt_model  --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/proj',
    dag=dag
)


def run_dbt_command():
    try:
        result = subprocess.run(['/home/airflow/.local/bin/dbt', 'test', '--profiles-dir', '/home/airflow/.dbt', '--project-dir', '/opt/airflow/proj'],
                                capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
        print(e.stderr)


dbt_data_quality_checks = BashOperator(
    task_id='dbt_data_quality_checks',
    bash_command=r'/home/airflow/.local/bin/dbt test --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/proj',
    dag=dag
)
elementary_reports = BashOperator(
      task_id="elementary_reports_generation",
      bash_command="/home/airflow/.local/bin/edr report",
      dag=dag
    )


# Set task dependencies
run_model1 >> dbt_data_quality_checks >> elementary_reports
