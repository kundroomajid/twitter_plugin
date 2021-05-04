#  Copyright (c) MAK 2021
#  Author : Kundroo Majid
#  Date : 28/04/2021

from airflow.exceptions import AirflowException

class TwitterConnectionNotFoundException(AirflowException):

    '''
    @:exception: TwitterConnectionNotFoundException, raised if no connection
    with connection id 'twitter_conn' is found in the meta-database
    '''

    def __init__(self,*args):
        if args:
            self.message = args[0]
        else:
            self.message = "No connection with id 'twitter_conn' defined"

    def __str__(self):
        if self.message:
            return "TwitterConnectionNotFoundException, {}".format(self.message)
        else:
            return "TwitterConnectionNotFoundException has been raised"


class ConfigVariableNotFoundException(AirflowException):
    '''
    @:exception: ConfigVariableNotFoundException, raised if no variable
    with key 'config' is found in the meta-database

    '''

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "No variable with key 'config' defined"

    def __str__(self):
        if self.message:
            return "ConfigVariableNotFoundException, {}".format(self.message)
        else:
            return "ConfigVariableNotFoundException has been raised"