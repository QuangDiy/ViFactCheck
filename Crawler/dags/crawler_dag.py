from airflow import DAG
from datetime import datetime
from airflow.decorators import task
from airflow.operators.python import PythonOperator

default_args ={
    'owner': 'you',
    'start_date': datetime(2023, 8, 22),  # UTC time
    'depends_on_past': False,
    'retries': 2,
}

with DAG(
    'Crawler_DAG',
    default_args=default_args,
    description='A automated crawler daily',
    schedule_interval='@daily',
    tags=['crawler'],
    catchup=False,
) as dag:
    
    @task
    def BM25_model():
        from BM25_fastapi import export_bm25_model
        export_bm25_model()
    @task
    def Bao_CP():
        from Baochinhphucrawler import BaoCP_df_to_DB
        BaoCP_df_to_DB()
    @task
    def Bao_TN():
        from Thanhniencrawler import Thanhnien_df_to_DB
        Thanhnien_df_to_DB()
    @task
    def Bao_VNE():
        from VnExpresscrawler import VNE_df_to_DB
        VNE_df_to_DB()
    BCP = PythonOperator(
        task_id="BCP_crawler",
        python_callable=Bao_CP,
    )
    BTN = PythonOperator(
        task_id="BTN_crawler",
        python_callable=Bao_TN,
    )
    BVNE = PythonOperator(
        task_id="VNE_crawler",
        python_callable=Bao_VNE,
    )
    exportbm25model = PythonOperator(
        task_id="Export_bm25_model",
        python_callable=BM25_model,
    ) 

BCP >> BTN >> BVNE >> exportbm25model