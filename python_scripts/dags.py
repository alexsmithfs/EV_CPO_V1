from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from raw_data_etl_pipeline import run_pipeline_rev_src_1
"""
# Define the DAG context
with DAG(
    dag_id="python_function_schedule_operator",
    start_date=datetime(2026, 1, 1),
    schedule_interval="0 12 * * *",   # CRON expression: Runs every day at 12:00 PM
    catchup=False
) as dag:

    # 3. Use PythonOperator to schedule the function
    run_python_task = PythonOperator(
        task_id="run_clean_data",
        python_callable=run_pipeline_rev_src_1
    )
"""