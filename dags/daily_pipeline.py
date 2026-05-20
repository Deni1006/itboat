from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, '/opt/airflow')

from scrapers.avito import scrape
from normalizers.avito import normalize

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='yacht_daily_pipeline',
    default_args=default_args,
    start_date=datetime(2026, 5, 14),
    schedule_interval='0 20 * * *',
    catchup=False,
) as dag:

    scrape_avito = PythonOperator(
        task_id='scrape_avito',
        python_callable=scrape,
    )

    normalize_avito = PythonOperator(
        task_id='normalize_avito',
        python_callable=normalize,
    )

    scrape_avito >> normalize_avito
