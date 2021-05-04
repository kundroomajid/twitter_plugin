#  Copyright (c) MAK 2021
#  Author : Kundroo Majid
#  Date : 28/04/2021

from airflow.utils.decorators import apply_defaults
from airflow.utils.email import send_email
from airflow.models.variable import Variable
from airflow.operators.python_operator import PythonOperator
from twitter_plugin.utils.exceptions import ConfigVariableNotFoundException
import json

class Email_Operator(PythonOperator):

    @apply_defaults
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def execute(self, context):

        message ="<h3> Dag Successfull </h3>"
        try:
            config = json.loads(Variable.get("config"))
            email = config['email']
        except NameError as e:
            raise ConfigVariableNotFoundException()

        send_email(
            to=email,
            subject='Airflow Notification',
            html_content=message
        )