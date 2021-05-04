from airflow import DAG
from  airflow import settings
from airflow.models import DagModel
from airflow.operators.dummy_operator import DummyOperator
from twitter_plugin.sensors.tweet_sensor import TweetSensor
from twitter_plugin.operators.email_operator import Email_Operator
from twitter_plugin.operators.tweet_etl_operator import TwitterETLOperator
import typing
from datetime import timedelta
import pendulum


dag = DAG(
    dag_id=str('Covid_Media_Bulliten_Update_ETL_DAG'),
    schedule_interval='0 0 10 * * *',
    catchup=False,
    default_args={
        'owner': 'MAK',
        'depends_on_past': False,
        'email': ['kundroomajid@gmail.com'],
        'email_on_failure': True,
        'start_date': pendulum.parse('2021-05-01 00:00:00'),
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    }
)
start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag, trigger_rule='none_failed')
check_tweet = TweetSensor(task_id='check_tweet',dag=dag,poke_interval=300, timeout=60 * 60 * 8)
notify_submission_success = Email_Operator(task_id='notify_submission_success', dag=dag, trigger_rule='none_failed',provide_context=True, python_callable=typing.Callable)
submission = TwitterETLOperator(task_id='get_and_process_tweet',extract_table_conn='extract_table_default',dag=dag,bulliten_tweet='bulliten_tweet')
start >> check_tweet >> submission >> notify_submission_success>> end


session = settings.Session()
try:
    qry = session.query(DagModel).filter(DagModel.dag_id == dag.dag_id)
    d = qry.first()
    d.is_paused = False
    session.commit()
except:
    session.rollback()
finally:
    session.close()