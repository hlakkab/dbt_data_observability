from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
        dag_id='dag_airflow_test1',
        default_args={
         'owner': 'you',
         'start_date': datetime(2024, 3, 14),  # Adjust as needed
         'retries': 1,
         'retry_delay': timedelta(minutes=5),
        },
        schedule_interval=None,  # Set a schedule if needed (e.g., '@daily')
) as dag:
 def say_hello():
  print("hello")


 say_hello_task = PythonOperator(
  task_id='say_hello',
  python_callable=say_hello,
 )