from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments for the tasks
default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'olist_ecommerce_data_pipeline',
    default_args=default_args,
    description='Olist E-commerce Data Pipeline',
    schedule='@daily',
    catchup=False,
) as dag:

    # 1. Ingest Raw CSV data into Bronze Layer (Parquet format)
    ingest_bronze = BashOperator(
        task_id='ingest_bronze_layer',
        bash_command='docker exec spark-master /opt/spark/bin/spark-submit /app/scripts/ingest_bronze.py',
    )

    # 2. Clean, cast, and deduplicate data into Silver Layer
    transform_silver = BashOperator(
        task_id='transform_silver_layer',
        bash_command='docker exec spark-master /opt/spark/bin/spark-submit /app/scripts/transform_silver.py',
    )

    # 3. Join tables into a Star Schema within the Gold Layer
    load_gold = BashOperator(
        task_id='load_gold_layer',
        bash_command='docker exec spark-master /opt/spark/bin/spark-submit /app/scripts/load_gold.py',
    )

    # 4. Export analytical models from Gold Layer to MySQL Production DW
    load_mysql = BashOperator(
        task_id='export_to_mysql_dw',
        bash_command='docker exec -u root spark-master /opt/spark/bin/spark-submit --jars /app/mysql-connector-java-8.0.28.jar /app/scripts/load_to_mysql.py',
    )

    # Define the strict processing dependency chain
    ingest_bronze >> transform_silver >> load_gold >> load_mysql