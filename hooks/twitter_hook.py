#  Copyright (c) MAK 2021
#  Author : Kundroo Majid
#  Date : 28/04/2021

from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException
from airflow.utils.log.logging_mixin import LoggingMixin
import tweepy


class TwitterHook(BaseHook):
    """
    Interact with Twitter API, using tweepy lib.
    """

    def __init__(self,
                 consumer_key=None,
                 consumer_secret=None,
                 access_token=None,
                 access_token_secret=None,
                 twitter_conn_id=None):
        """
        Takes twitter credentials like consumer_key, consumer_secret, 
        access_token, and access_token_secret which can be obtained by creating 
        an app in twitter developer account. https://developer.twitter.com/en/docs/getting-started

        :param consumer_key: Twitter app consumer_key
        :param consumer_secret: Twitter app consumer_secret
        :param access_token: Twitter app access_token
        :param access_token_secret: Twitter app access_token_secret
        :param twitter_conn_id: connection that has Twitter App credentials like  consumer_key etc
        :type consumer_key: str
        :type consumer_secret: str
        :type access_token: str
        :type access_token_secret: str
        :type twitter_conn_id: str
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret


    def get_tweepy_api(self, wait_on_rate_limit=True, wait_on_rate_limit_notify=True):
        log = LoggingMixin().log
        try:
            auth = tweepy.AppAuthHandler(self.consumer_key, self.consumer_secret)
            api = tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit,
                         wait_on_rate_limit_notify=wait_on_rate_limit_notify)
            log.info("Using connection to twitter API ")
            return api
        except Exception:
            raise AirflowException("Twitter credentials not valid")
