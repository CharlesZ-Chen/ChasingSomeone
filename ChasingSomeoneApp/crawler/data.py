#!/usr/bin/env python
# -*- coding: utf-8 -*-

'data application use'

__author__ = 'Quan Zhang'

from tweepy import OAuthHandler
# data-----------------------------------

consumer_key = "0mnQdA5pm4lBYkM2hMXxfa5sp"
consumer_secret = "uUAdSfjhmjLNfXlxZe3vrA0Bmvaku88cPy333MT0zX3LV5dAve"


access_token = "3991423984-aSDrrk4wFuiDcvlni3234impHR7rQgUupFMeUEI"
access_token_secret = "Iedx6e7Xdx6aY3OUdNMbRUOw6ivQuoZ77dLScgTe0rqjX"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

if __name__=='__main__':
    pass