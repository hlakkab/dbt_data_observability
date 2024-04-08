import yaml
import subprocess


def create_models(table_name, columns=None):
    models = []
    if columns:
        for column in columns:
            model = {
                "name": f"model_{table_name}_{column}",
                "columns": [{"name": column}],
                "tests": ["test1.yml", "test2"]
            }
            models.append(model)
    else:
        model = {
            "name": f"model_{table_name}",
            "tests": ["test1.yml", "test2"]
        }
        models.append(model)
    return models


def generate_yaml(models):
    yaml_content = {"models": models}
    with open("models.yaml", "w") as yaml_file:
        yaml.dump(yaml_content, yaml_file)


def main():
    table_name = "ma_table"
    models = create_models(table_name)
    generate_yaml(models)


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


def generate_yaml_file3(table_name, error_count, error_period, warn_count, warn_period):
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
                            "error_after": {"count": error_count, "period": error_period}
                        }
                    }
                ]
            }
        ]
    }


    with open(f"C:/Users/NEMO/PycharmProjects/dbt5/proj/models/example/{table_name}_freshnes.yml", 'w') as yaml_file:
        yaml.dump(yaml_content, yaml_file, default_flow_style=False, indent=2)


"""
# Example usage:
table_name = 'freshnes_test'
error_count = 12
error_period = 'day'
warn_count = 6
warn_period = 'hour'
file_name = 'config.yml'
yaml_file_path = generate_yaml_file3(table_name, error_count, error_period, warn_count, warn_period)
print("YAML file has been generated successfully.")
"""





def run_dbt_command(bash_command, working_directory):
    try:
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, check=True, cwd=working_directory)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If the command fails, you can handle the error here
        return f"Error occurred: {e}\n{e.stderr}"

# Define your bash command
bash_command = r'dbt test'

# Specify the directory where you want to run the command
working_directory = 'C:/Users/NEMO/PycharmProjects/dbt5/proj'

# Run the dbt command and capture the result
dbt_command_result = run_dbt_command(bash_command, working_directory)
print(dbt_command_result)
