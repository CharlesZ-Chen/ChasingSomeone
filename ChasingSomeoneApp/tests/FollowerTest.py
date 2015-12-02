__author__ = 'charleszhuochen'
import json

from django.test import TestCase
from django.test import Client

from ChasingSomeoneApp.models.UserProfile import User
from ChasingSomeoneApp.views import TWAccountView
from ChasingSomeoneApp.views import  AccountView
from ChasingSomeoneApp.models.TwAccount import TwAccount
from ChasingSomeoneApp.models.Follower import Follower
from ChasingSomeoneApp.tests import Utils

url_add_follower = '/ChasingSomeone/add_follower/'
url_save_account = '/ChasingSomeone/save_account/'
url_delete_follower = '/ChasingSomeone/delete_follower/'

class TestFollwerView(TestCase):

    def set_up(self):
        setup_dict = Utils.set_up()
        self.client = setup_dict['client']
        self.user = setup_dict['user']

    def test_add_follower(self):
        self.set_up()
        flr_name = 'testFollower'
        ajax_dict = {'flr_name': flr_name}
        response = Utils.ajax_post_json(self.client, url_add_follower, ajax_dict)
        response_data = json.loads(response.content)
        self.assertEqual(True, 'flr_id' in response_data)
        if response.content != 'False':
            ajax_dict = {'flr_name': 'testFollower',
                         'act_type': 'twitter',
                         'act_id': None,
                         'screen_name': 'charleszhuochen'}
            response = Utils.ajax_post_json(self.client, url_save_account, ajax_dict)
            self.assertEqual('True', response.content)
            self.assertEqual(True, TwAccount.objects.filter(follower__name=flr_name).exists())
        self.assertEqual(True, Follower.objects.filter(name=flr_name).exists())
        return flr_name

    def test_delete_follower(self):
        flr_name = self.test_add_follower()
        ajax_dict = {'flr_name': flr_name}
        response = Utils.ajax_post_json(self.client, url_delete_follower, ajax_dict)
        self.assertEqual('True', response.content)
        self.assertEqual(False, Follower.objects.filter(name=flr_name).exists())
        self.assertEqual(False, TwAccount.objects.filter(follower__name=flr_name).exists())

    def test_delete_non_exsit_follower(self):
        self.set_up()
        flr_name = 'notExistFollower'
        ajax_dict = {'flr_name': flr_name}
        response = Utils.ajax_post_json(self.client, url_delete_follower, ajax_dict)
        self.assertEqual('False', response.content)




