 # -*- coding: utf-8 -*-

from django.test import TestCase
from django.test import Client
# Create your tests here.
from ChasingSomeoneApp.views import TwStatusView
from ChasingSomeoneApp.models import TwFollower, TwStatus
from ChasingSomeoneApp.models.UserProfile import User
import time

class TestTwFollower(TestCase):
    def test_save(self):
        user = User()
        user.username = 'testUser'
        user.save()
        get_user = User.objects.get(username="testUser")
        follower = TwFollower()
        follower.screen_name = "test"
        follower.follower_id = "123456"
        follower.user = get_user
        follower.save()

        self.assertEqual(TwFollower.objects.filter(follower_id="123456").exists(), True)

        status = TwStatus()
        status.id = u'107809348885028864'
        status.twFollower = follower
        status.text = u'hello world'
        raw_time = 'Sun Aug 28 13:38:46 +0000 2011'
        # ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(raw_time,'%a %b %d %H:%M:%S +0000 %Y'))
        ts = '2015-11-03 05:07:07'
        status.created_at = ts
        status.save()
        self.assertEqual(TwStatus.objects.filter(id=u'107809348885028864').exists(), True)

class TestAuthView(TestCase):
    def test_login(self):
        client = Client()
        client.post('/ChasingSomeone/register/', {'username': 'demoUser', 'password': '123'})
        self.assertEqual(User.objects.filter(username="demoUser").exists(), True)
        response = client.post('/ChasingSomeone/login/', {'username': "testUser1", 'password': '123'})
        self.assertEqual(response.status_code, 200)
        response = client.get('/ChasingSomeone/home/')
        self.assertEqual(response.status_code, 302) #rediect to login page
        client.post('ChasingSomeone/login/', {'username': "demoUser", 'password': '123'})
        # response = client.get('/ChasingSomeone/home/')
        # self.assertEqual(response.status_code, 200)
