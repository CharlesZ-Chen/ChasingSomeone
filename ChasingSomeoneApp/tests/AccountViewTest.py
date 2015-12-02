__author__ = 'charleszhuochen'
import json

from django.test import TestCase
from django.test import Client

from ChasingSomeoneApp.views import AccountView, TWAccountView
from ChasingSomeoneApp.models.Follower import Follower
from ChasingSomeoneApp.models.UserProfile import User
from ChasingSomeoneApp.models.TwAccount import TwAccount
from ChasingSomeoneApp.tests import Utils

url_verify_account = '/ChasingSomeone/verify_account/'
url_delete_account = '/ChasingSomeone/delete_account/'
url_save_account = '/ChasingSomeone/save_account/'


class TestAccountView(TestCase):
    def set_up(self):
        setup_dict = Utils.set_up()
        self.client = setup_dict['client']
        self.user = setup_dict['user']

    def test_verify_account(self):
        self.set_up()
        '''a real account would pass verification and return the details of verified account'''
        ajax_dict = {'act_type': 'twitter',
                  'flr_name': None,
                  'act_id': None,
                  'screen_name': 'charleszhuochen'}
        json_data = json.dumps(ajax_dict)
        response = self.client.post(url_verify_account, json_data, 'json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual('{"act_id": "3991423984", "screen_name": "charleszhuochen"}', response.content)

    def test_verify_non_exist_account(self):
        self.set_up()
        '''an un-exist account would failed verification
        and would get '404' indicate that can not find this account'''
        ajax_dict = {'act_type': 'twitter',
                  'flr_name': None,
                  'act_id': None,
                  'screen_name': 'thisisnotauseribelievenooneusethisasaccountname'}
        response = Utils.ajax_post_json(self.client, url_verify_account, ajax_dict)
        self.assertEqual('404', response.content)

    def test_verify_exist_account(self):
        self.set_up()
        '''verify a new account while the follower already have one will return False'''
        follower = Follower(name='testFollower', user=self.user)
        follower.save()
        tw_account = TwAccount(follower=follower,act_id='3991423984', screen_name='charleszhuochen')
        tw_account.save()

        ajax_dict = {'act_type': 'twitter',
                  'flr_name': 'testFollower',
                  'act_id': None,
                  'screen_name': '_QuanZhang_'}
        response = Utils.ajax_post_json(self.client, url_verify_account, ajax_dict)
        self.assertEqual('False', response.content)

    def test_http_delete_account(self):
        self.set_up()
        '''normal case: delete an exist account would return True'''
        flr_name = 'testFollower'
        follower = Follower(name=flr_name, user=self.user)
        follower.save()
        tw_account = TwAccount(follower=follower, act_id='3991423984', screen_name='charleszhuochen')
        tw_account.save()
        '''before delete, TwAccount has this account'''
        self.assertEqual(True, TwAccount.objects.filter(follower__name=flr_name).exists())
        ajax_dict = {'flr_name': 'testFollower',
                     'act_type': 'twitter'}
        response = Utils.ajax_post_json(self.client, url_delete_account, ajax_dict)
        '''after delete, TwAccount does not has this account anymore'''
        self.assertEqual('True', response.content)
        self.assertEqual(False, TwAccount.objects.filter(follower__name=flr_name).exists())

    def test_http_save_account(self):
        self.set_up()
        '''normal case: an exist follower save a new account, the account would save in to database and return True'''
        flr_name = 'testFollower'
        follower = Follower(name=flr_name, user=self.user)
        follower.save()
        ajax_dict = {'flr_name': flr_name,
                     'act_type': 'twitter',
                     'act_id': None,
                     'screen_name': 'charleszhuochen'}
        '''save_account would return True'''
        response = Utils.ajax_post_json(self.client, url_save_account, ajax_dict)
        self.assertEqual('True', response.content)

    def test_http_save_account_with_non_exist_follower(self):
        self.set_up()
        '''if try to save an account to a non-exist follower, then will get a False'''

        flr_name = 'testFollower'
        ajax_dict = {'flr_name': flr_name,
                     'act_type': 'twitter',
                     'act_id': None,
                     'screen_name': 'charleszhuochen'}
        '''if post an un-existed flr_name, save_account would return False'''
        response = Utils.ajax_post_json(self.client, url_save_account, ajax_dict)
        self.assertEqual('False', response.content)

    def test_http_save_account_with_exist_account(self):
        self.set_up()
        '''Since this user already has a twitter account after first save, then the second save would get a False'''

        flr_name = 'testFollower'
        follower = Follower(name=flr_name, user=self.user)
        follower.save()
        ajax_dict = {'flr_name': flr_name,
                     'act_type': 'twitter',
                     'act_id': None,
                     'screen_name': 'charleszhuochen'}
        Utils.ajax_post_json(self.client, url_save_account, ajax_dict)
        ajax_dict = {'flr_name': flr_name,
                     'act_type': 'twitter',
                     'act_id': None,
                     'screen_name': '_QuanZhang_'}
        response = Utils.ajax_post_json(self.client, url_save_account, ajax_dict)
        self.assertEqual('False', response.content)

    def test_http_save_fake_account_with_exist_account(self):
        self.set_up()
        '''Since this user already has a twitter account, then no matter the new twitter account is fake or real,
        http_save_account() would return a false indicate that this user already has a twitter account
        (notice, in this case currently we CANNOT distinguish non-exist follower from already exist account
        since both cases will return False)'''

        flr_name = 'testFollower'
        follower = Follower(name=flr_name, user=self.user)
        follower.save()
        ajax_dict = {'flr_name': flr_name,
                     'act_type': 'twitter',
                     'act_id': None,
                     'screen_name': 'charleszhuochen'}
        Utils.ajax_post_json(self.client, url_save_account, ajax_dict)
        ajax_dict = {'flr_name': flr_name,
                     'act_type': 'twitter',
                     'act_id': None,
                     'screen_name': 'fakeuserfakeuserthisisfakeuseribek'}
        response = Utils.ajax_post_json(self.client, url_save_account, ajax_dict)
        self.assertEqual('False', response.content)

    def test_http_save_fake_account(self):
        self.set_up()
        ''' if an user try to save a fake account, then the verifycation module would return '404' indicates that
        this account could not pass verification since could not find it on that social website '''

        flr_name = 'testFollower'
        follower = Follower(name=flr_name, user=self.user)
        follower.save()
        ajax_dict = {'flr_name': flr_name,
                     'act_type': 'twitter',
                     'act_id': None,
                     'screen_name': 'fakeuserfakeuserthisisfakeuseribek'}
        response = Utils.ajax_post_json(self.client, url_save_account, ajax_dict)
        self.assertEqual('404', response.content)
