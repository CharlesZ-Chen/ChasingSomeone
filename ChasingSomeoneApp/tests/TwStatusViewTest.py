__author__ = 'charleszhuochen'

import json

from django.test import TestCase

from ChasingSomeoneApp.views import TwStatusView, QrStatusView
from ChasingSomeoneApp.models.Follower import Follower
from ChasingSomeoneApp.models.TwAccount import TwAccount
from ChasingSomeoneApp.models.TwStatus import TwStatus
from ChasingSomeoneApp.models.QrAccount import QrAccount
from ChasingSomeoneApp.tests import Utils

url_refresh_status_site = '/ChasingSomeone/refresh_status_site/'
url_refresh_status_flr = '/ChasingSomeone/refresh_status_flr/'

class TwStatusViewTest(TestCase):
    def set_up(self):
        setup_dict = Utils.set_up()
        self.client = setup_dict['client']
        self.user = setup_dict['user']

    def test_refresh_status(self):
        self.set_up()
        follower = Follower(name='testFollower', user=self.user)
        follower.save()
        tw_account = TwAccount(follower=follower, act_id='3991423984', screen_name='charleszhuochen')
        tw_account.save()

        tw_account_list = [tw_account, ]
        since_id = None
        status_list = TwStatusView.refresh_status(tw_account_list, since_id)
        print(status_list[0]['created_at'])
        latest_status = TwStatus.objects.get(id=status_list[0]['id'])
        print(latest_status.created_at)
        self.assertEqual(10, len(status_list))
        since_id = int(status_list[0]['id'])
        status_list = TwStatusView.refresh_status(tw_account_list, since_id)
        self.assertEqual(0, len(status_list))

class StatusViewTest(TestCase):
    def set_up(self):
        setup_dict = Utils.set_up()
        self.client = setup_dict['client']
        self.user = setup_dict['user']
        flr_name = 'testFollower'
        self.follower = Follower(name=flr_name, user=self.user)
        self.follower.save()
        self.tw_account = TwAccount(follower=self.follower, act_id='3991423984', screen_name='charleszhuochen')
        self.tw_account.save()
        self.qr_account = QrAccount(follower=self.follower, user_name='quan-zhang-27')
        self.qr_account.save()

    def test_refresh_status(self):
        self.set_up()

        ajax_dict = {'site_type': 'quora'}
        response = Utils.ajax_post_json(self.client, url_refresh_status_site, ajax_dict)
        status_list = json.loads(response.content)['status_list']
        self.assertEqual(10, len(status_list))
        print status_list

        # since_id = status_list[0]["id"]
        # ajax_dict = {'site_type': 'twitter',
        #              'since_id': since_id}
        # response = Utils.ajax_post_json(self.client, url_refresh_status_site, ajax_dict)
        # status_list = json.loads(response.content)['status_list']
        # self.assertEqual(0, len(status_list))

    def test_refresh_status_flr(self):
        self.set_up()

        ajax_dict = {'flr_name': self.follower.name}
        response = Utils.ajax_post_json(self.client, url_refresh_status_flr, ajax_dict)
        status_list = json.loads(response.content)['status_list']
        # for status in status_list:
        #     print "%s\t" % status['act_type']
        #     print status.get('time_stamp', None)
        #     print "\n"
        ajax_dict = {'flr_name': self.follower.name,
                     'lt_st_time': '2015-12-02 03:49:00'}
        response = Utils.ajax_post_json(self.client, url_refresh_status_flr, ajax_dict)
        status_list = json.loads(response.content)['status_list']
        for status in status_list:
            print "%s\t" % status['act_type']
            print status.get('time_stamp', None)
            print "\n"
class QrStatusViewTest(TestCase):
    def set_up(self):
        setup_dict = Utils.set_up()
        self.client = setup_dict['client']
        self.user = setup_dict['user']

    def test_refresh_status(self):
        self.set_up()
        flr_name = 'testFollower'
        follower = Follower(name=flr_name, user=self.user)
        follower.save()
        qr_account = QrAccount(follower=follower, user_name='quan-zhang-27')
        qr_account.save()

        qr_account_list = [qr_account, ]

        status_list =  QrStatusView.refresh_status(qr_account_list)
        print status_list
