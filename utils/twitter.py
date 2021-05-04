#  Copyright (c) MAK 2021
#  Author : Kundroo Majid
#  Date : 28/04/2021

import json
from datetime import date
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable
from airflow.utils.log.logging_mixin import LoggingMixin
from twitter_plugin.utils.exceptions import ConfigVariableNotFoundException
from twitter_plugin.hooks.twitter_hook import TwitterHook
from twitter_plugin.utils.exceptions import TwitterConnectionNotFoundException


def check_if_tweet_is_avalaible(twitter_account_id=None, since_id=None, find_param=None, **kwargs):
    """
    This method tweepy api via TwitterHook to check if a tweet from a specific twitter_account
    containing a specific search_string or not
    :param: twitter_account_id : for which tweets are to be fetched
    :param: since_id : airflow execution date of the dag
    :return: tweet_id
    """
    log = LoggingMixin().log
    try:
        # Load Configuration Data
        config = json.loads(Variable.get("config"))
        log.info("Config found")

    except AirflowException as e:
        log.error("Config missing")
        raise ConfigVariableNotFoundException()

    try:
        twitter_account_id = config['twitter_account_id']
    except KeyError as e:
        raise AirflowException('Missing Twitter Account Id in config variable')

    try:
        since_id = config['since_id']
    except KeyError as e:
       log.warn("Since id missing")

    try:
        find_param = config['find_param'].lower()
    except KeyError as e:
        raise AirflowException('Missing Find Param in config variable')

    try:
        twitter_credentials = BaseHook.get_connection("twitter_default")
        twitter_credentials = json.loads(twitter_credentials.extra)
        consumer_key = twitter_credentials['consumer_key']
        consumer_secret = twitter_credentials['consumer_secret']
        access_token = twitter_credentials['access_token']
        access_token_secret = twitter_credentials['access_token_secret']

    except AirflowException as e:
        raise TwitterConnectionNotFoundException()

    twitter_hook = TwitterHook(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    tweepy_api = twitter_hook.get_tweepy_api()
    today = date.today()
    curr_date = today.strftime("%d-%m-%Y")
    # try to get tweet related to covid media bulliten from @diprjk handle

    tweets = tweepy_api.user_timeline(id=twitter_account_id, since_id=since_id, count=1000,exclude_replies=True, include_rts=False, tweet_mode="extended")
    if len(tweets) > 0:
        # find_param = "Media Bulletin on Novel".lower()
        log.info("Found : {}  tweets".format(len(tweets) + 1))
        # loop over all extracted tweets and
        # if tweet.full_text contains string "Media Bulletin On Novel"
        # then we got our concerned tweet and save its tweet_id
        image_urls = []
        for tweet in tweets:
            tweet_date = tweet.created_at
            tweet_date = tweet_date.strftime("%d-%m-%Y")
            text = tweet.full_text.lower()
            if find_param in text and tweet_date == curr_date:
                bulletin_tweet_id = tweet.id
                print('Tweet found')
                # save bulliten tweet id as environ variable or on file and then use in next run
                log.info("Tweet ID: {}  TEXT : {} ".format(bulletin_tweet_id, tweet.full_text))
                if 'media' in tweet.entities:
                    for media in tweet.extended_entities['media']:
                        image_urls.append(media['media_url'])
                    detail_image_url = image_urls[2]
                    log.info("Tweet Image Url: {} ".format(detail_image_url))
                else:
                    log.info("No media found")
                    #skip the processing and end dag
                    return False
                data = {"tweet_id":bulletin_tweet_id,"tweet_date":tweet_date,"media_url": detail_image_url}
                Variable.set("bulliten_tweet", json.dumps(data))
                return True
            else:
                pass
        else:
            log.info("No tweets related to {} found".format(find_param))
            return False

    else:
        log.info("No tweets found!")
        return False
