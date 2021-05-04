#  Copyright (c) MAK 2021
#  Author : Kundroo Majid
#  Date : 28/04/2021

from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from twitter_plugin.utils.twitter import check_if_tweet_is_avalaible


class TweetSensor(BaseSensorOperator):

    @apply_defaults
    def __init__(self,
                 *args,
                 **kwargs):
        super(TweetSensor, self).__init__(*args, **kwargs)

    def poke(self, context):
        self.log.info("Poking Tweet Sensor and checking for tweet avalability :")
        ret_value = check_if_tweet_is_avalaible()
        return bool(ret_value)