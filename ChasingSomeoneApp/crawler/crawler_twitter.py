#!/usr/bin/env python
# -*- coding: utf-8 -*-

'main class of crawler, call add_follower() and get_status()'

__author__ = 'Quan Zhang'

import sys
sys.path.append('../')

from tweepy import API
from tweepy import *
from ChasingSomeoneApp.crawler import data
from urllib2 import URLError


class Crawler_twitter(object):
    api = API(data.auth)

    def __init__(self):
        self.__class__.api = API(data.auth)

    def add_follower(self, *args, **kwargs):
        # unique id number
        id = kwargs.get('id')
        # string after character @
        screen_name = kwargs.get('screen_name')

        if not id and not screen_name:
            return False
        try:
            user = self.api.get_user(id = id, screen_name = screen_name)
            # print user
            got_screen_name = user._json.get('screen_name')
            got_id = str(user._json.get('id'))
            got_name = user._json.get('name')
            # print got_id, got_name, got_screen_name
            # print id, screen_name

            if (id and id != got_id and id != got_name) or\
                    (screen_name and screen_name != got_screen_name):
                print 'Json Error from add_follower'
                return False
            return {'id': got_id, 'screen_name': screen_name}
        except TweepError, e:
            print 'TweepError from add_follower', e
            return False
        except URLError, e:
            print 'Network Error from add_follower', e
            return False
        except Exception, e:
            print 'Other Error from add_follower', e
            return False


    def get_status(self, *args, **kwargs):
        id = kwargs.get('id')
        screen_name = kwargs.get('screen_name')
        tweets = []
        if not id and not screen_name:
            return []
        try:
            timeline =  self.api.user_timeline(**kwargs)
            for tweet in timeline:
                tweets.append(tweet._json)
            return tweets
        except TweepError, e:
            print 'TweepError from get_status', e
            return []
        except URLError, e:
            print 'Network Error from get_status', e
            return []
        except Exception, e:
            print 'Other Error from get_status', e
            return []

if __name__ == '__main__':
    craw = Crawler_twitter()
    # print craw.api.get_user(id = '51248642')._json
    print craw.add_follower(id = '51248642')
    # print craw.add_follower(id = 'Matthew Perry', screen_name = 'matthewperryfan')
    print craw.api.user_timeline(id = '30653573')[0]._json
    # print craw.get_status(id = 'Matthew Perry', screen_name = 'matthewperryfan')

# api = API(auth)
# test = api.get_user(id = 'Matthew Perry', screen_name = 'matthewperryfan')
# print test
# test = api.get_user(id = 'colin_27', screen_name = 'colin_27')
# print test
# public_tweets = api.user_timeline(id = 'matthewperryfan', screen_name = 'Matthew Perry')
# for tweet in public_tweets:
#     print tweet._json