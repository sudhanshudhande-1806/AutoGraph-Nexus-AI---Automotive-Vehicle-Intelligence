from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime


def extract():

    print(
        "Extract Vehicle Data"
    )


def transform():

    print(
        "Transform Vehicle Data"
    )


def load():

    print(
        "Load Vehicle Data"
    )


with DAG(

    dag_id="vehicle_pipeline",

    start_date=datetime(
        2026,
        1,
        1
    ),

    schedule="@daily",

    catchup=False,

    tags=["autograph"]

) as dag:

    extract_task = PythonOperator(

        task_id="extract",

        python_callable=extract

    )

    transform_task = PythonOperator(

        task_id="transform",

        python_callable=transform

    )

    load_task = PythonOperator(

        task_id="load",

        python_callable=load

    )

    extract_task >> transform_task >> load_task