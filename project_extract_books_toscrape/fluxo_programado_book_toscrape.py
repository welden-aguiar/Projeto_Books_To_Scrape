from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_arguments = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email':'nome@email.com',
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2021, 12, 1, 15, 00)
}

with DAG(
    'projeto_books_toscrape',
    default_args = default_arguments,
    description = 'This DAG controls the flow of data extraction from books.toscrape website, transformation and loading in DW.',
    schedule_interval = timedelta(hours=1),
    catchup=False
) as dag:
    extraction = BashOperator(
        task_id='extraction',
        bash_command="""
            cd /home/$USER/Projects/project_extract_books_toscrape
            python3 extrair_dados_books_toscrape.py
        """
    )

    transformation_load = BashOperator(
        task_id='transformation_load',
        bash_command="""
            cd /home/$USER/Projects/project_extract_books_toscrape
            python3 tranformation_load.py
        """
    )

    extraction >> transformation_load
