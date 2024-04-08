import yaml
import os
from datetime import datetime


def generate_model_based_on_table(table_name):
    sql_content = f"""
-- Automatically generated SQL file for table: {table_name}

with {table_name}_model as (
    select * from public.{table_name}
),
final as (
    select
        *
    from {table_name}_model
)
select * from final;
"""

    with open(f"C:/Users/NEMO/PycharmProjects/dbt5/proj/models/example/{table_name}_model.sql", 'w') as sql_file:
        sql_file.write(sql_content)


def is_model_created(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)


def generate_yaml_file_for_freshness_test(table_name, warn_count, warn_period):
    yaml_content = {
        "version": 2,
        "sources": [
            {
                "name": "public",
                "database": "postgres",
                "loaded_at_field": "creation_date",
                "tables": [
                    {
                        "name": table_name,
                        "freshness": {
                            "warn_after": {"count": warn_count, "period": warn_period},
                        }
                    }
                ]
            }
        ]
    }

    with open(f"C:/Users/NEMO/PycharmProjects/dbt5/proj/models/example/{table_name}_freshnes.yml", 'w') as yaml_file:
        yaml.dump(yaml_content, yaml_file, default_flow_style=False, indent=2)


def generate_dag_based_on_freshness_test(model_name, anomaly_number, anomaly_unit, timestamp_column):
    current_date = datetime.now()
    sql_content = f"""from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


# Define the default arguments for the DAG
default_args = {{
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime({current_date.year}, {current_date.month}, {current_date.day}),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'is_paused_upon_creation': False
}}

# Create the DAG with the specified schedule interval
dag = DAG('dag___{model_name}', default_args=default_args, schedule_interval=timedelta(days=1))


run_model1 = BashOperator(
    task_id='run_model1',
    bash_command=r'/home/airflow/.local/bin/dbt run --models {model_name}   --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/proj',
    dag=dag
)

dbt_data_quality_checks = BashOperator(
    task_id='dbt_data_quality_checks',
    bash_command=r'/home/airflow/.local/bin/dbt test --select "elementary_freshness_anomalies_{model_name}_{anomaly_number}_{anomaly_unit}_{timestamp_column} " --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/proj',
    dag=dag
)

run_model1 >> dbt_data_quality_checks

"""

    with open(f"C:/Users/NEMO/PycharmProjects/dbt5/dags/{model_name}_model.py", 'w') as sql_file:
        sql_file.write(sql_content)


generate_dag_based_on_freshness_test("freshnes_test", "1", "hour", "created_at")
