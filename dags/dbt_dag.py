from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import subprocess
import re


# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 31),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG with the specified schedule interval
dag = DAG('dag___fresh', default_args=default_args, schedule_interval=timedelta(days=1))

# -------------


def extract_test_results(log_string):
    test_results = {}
    # Split the log string by the pattern 'RUN test'
    test_sections = re.split(r'\d{2}:\d{2}:\d{2}', log_string)[1:]
    for section in test_sections:
        pass_test_name_match = re.search(r'PASS (\S+)\s+(\S+)', section)
        fail_test_name_match = re.search(r'FAIL (\S+)\s+(\S+)', section)
        if pass_test_name_match:
            test_name = pass_test_name_match.group(1)
            print(test_name)
            # Extract the test result
            test_result_match = re.search(r'PASS|FAIL', section)
            if test_result_match:
                test_result = test_result_match.group()
                test_results[test_name] = test_result
        if fail_test_name_match:
            test_name = fail_test_name_match.group(2)
            print(test_name)
            # Extract the test result
            test_result_match = re.search(r'PASS|FAIL', section)
            if test_result_match:
                test_result = test_result_match.group()
                test_results[test_name] = test_result
    return test_results


class CustomBashOperator(BaseOperator):
    """
    Custom BashOperator to capture entire output and push it to XCom.
    """

    @apply_defaults
    def __init__(self, bash_command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bash_command = bash_command

    def execute(self, context):
        try:
            # Run the bash command and capture the output
            result = subprocess.run(self.bash_command, shell=True, capture_output=True, text=True, check=False)
            output = result.stdout
            print(output)
            filtered_output = extract_test_results(output)
            # Push the entire output to XCom
            context['task_instance'].xcom_push(key='dbt_test_output', value=filtered_output)
        except subprocess.CalledProcessError as e:
            self.log.error(f"Error occurred: {e}")
            raise e

# -------------


dbt_data_quality_checks = CustomBashOperator(
    task_id='dbt_data_quality_checks',
    bash_command=r'/home/airflow/.local/bin/dbt test --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/proj',
    dag=dag
)


# Function to print and handle dbt command result
def print_and_handle_dbt_command_result(**kwargs):
    print("Result of dbt command:")
    print("-------")

    ti = kwargs['ti']
    dbt_command_result = ti.xcom_pull(key='dbt_test_output')
    print(dbt_command_result)
    # Extract all lines of the output and concatenate them into a single string
    print("-----------")


# Task to run function to print and handle dbt command result
handle_dbt_result = PythonOperator(
    task_id='handle_dbt_result',
    python_callable=print_and_handle_dbt_command_result,
    provide_context=True,
    dag=dag
)

dbt_data_quality_checks >> handle_dbt_result
