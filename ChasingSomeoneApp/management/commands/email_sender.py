#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quan Zhang'

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Max
from ChasingSomeoneApp.models.UserProfile import UserProfile
from ChasingSomeoneApp.models.Follower import Follower
from ChasingSomeoneApp.models.TwAccount import TwAccount
from ChasingSomeoneApp.models.TwStatus import TwStatus
from ChasingSomeoneApp.models.QrAccount import QrAccount
from ChasingSomeoneApp.models.QrStatus import QrStatus
from ChasingSomeoneApp.crawler.crawler_twitter import Crawler_twitter
from ChasingSomeoneApp.crawler.crawler_quora import Crawler_quora
import time

class Command(BaseCommand):
    help = 'Crawl the Twitter and Quora, send mail to user'

    def add_arguments(self, parser):
        pass

    def my_send_email(self, notification, target_email):
        # email = 'charleszhuochen@gmail.com'
        # msg += "http://127.0.0.1:8000"
        subject = 'You\'ve got new notification!'
        msg = notification
        send_mail(subject,
                  msg,
                  settings.EMAIL_HOST_USER, [target_email], fail_silently=True)

    def get_user_list(self):
        try:
           user_list = UserProfile.objects.all()
           return user_list
        except UserProfile.DoesNotExist:
            print 'Can not get user list from UserProfile'
            return []

    def get_follower_list(self, user_profile):
        if not user_profile:
            print 'Empty argument in get_follower_list'
            return []
        try:
            follower_list = list(Follower.objects.filter(user=user_profile.user))
            return follower_list
        except Follower.DoesNotExist:
            print 'Can not get follower list from Follower'

    def get_twaccount(self, follower):
        if not follower:
            print 'Empty argument in get_twaccount'
            return None
        try:
            twaccount = TwAccount.objects.get(follower=follower)
            return twaccount
        except TwAccount.DoesNotExist:
            print 'Can not get Twitter account from TwAccount'

    def get_qraccount(self, follower):
        if not follower:
            print 'Empty argument in get_qraccount'
            return None
        try:
            qraccount = QrAccount.objects.get(follower=follower)
            return  qraccount
        except QrAccount.DoesNotExist:
            print 'Can not get Twitter account from TwAccount'

    def is_update_twitter(self, twaccount):
        try:
            # max_id_status = TwStatus.objects.raw('select max(id) from ChasingSomeoneApp_twstatus')
            status = TwStatus.objects.all().aggregate(Max('id'))
            max_id_status = status['id__max']
        except TwStatus.DoesNotExist:
            print 'Can not get status from TwStatus'
            max_id_status = None
        crawler = Crawler_twitter()
        status_list = None
        if max_id_status:
            status_list = crawler.get_status(id=twaccount.act_id, screen_name=twaccount.screen_name,
                                                     since_id=int(max_id_status))
        else:
            status_list = crawler.get_status(id=twaccount.act_id, screen_name=twaccount.screen_name)
        if not status_list:
            print 'Can not get posts from user\'s homepage'
            return False
        try:
            self.update_twitter_status(twaccount, status_list)
        except KeyError:
            print 'Error occured when updates twitter status'
            return False
        return True

    def is_update_quora(self, qraccount):
        try:
            # max_id_status = TwStatus.objects.raw('select max(id) from ChasingSomeoneApp_twstatus')
            status = QrStatus.objects.all().aggregate(Max('time_stamp'))
            max_id_status = status['time_stamp__max']
        except QrStatus.DoesNotExist:
            print 'Can not get status from TwStatus'
            max_id_status = None
        crawler = Crawler_quora()
        status_list = crawler.get_status(user_name=qraccount.user_name)

        if not status_list:
            print 'Can not get posts from user\'s homepage'
            return False
        try:
            if not self.update_quora_status(qraccount, status_list):
                return False
        except KeyError:
            print 'Error occured when updates quora status'
            return False
        return True

    def update_twitter_status(self, twaccount, status_list):
        for json_status in status_list:
            status = TwStatus()
            status.id = json_status['id_str']
            status.twAccount = twaccount
            status.text = json_status['text']
            transfer_ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(json_status['created_at'],
                                                                               '%a %b %d %H:%M:%S +0000 %Y'))
            status.created_at = transfer_ts
            status.save()


    def update_quora_status(self, qraccount, status_list):
        is_update = False
        for json_status in status_list:
            if not QrStatus.objects.filter(target=json_status['target'], action_type=json_status['action_type']):
                status = QrStatus()
                status.user_profile_name = json_status['user_name']
                status.qrAccount = qraccount
                status.target = json_status['target']
                status.url_target = json_status['url']
                status.action_type = json_status['action_type']
                status.user_profile_img = json_status['user_profile_image']
                status.time_stamp = json_status['time_stamp']
                status.save()
                is_update = True
        return is_update

    def handle(self, *args, **options):
        accout_list = self.get_user_list()
        # list of UserProfile objects
        if len(accout_list) == 0:
            return

        notification = 'You got new notification from:\n'
        for accout in accout_list:
            # accout : UserProfile object
            isUpdated = False
            follower_list = self.get_follower_list(accout)
            # list of follower objects

            for follower in follower_list:
                # follower : follower object

                twaccount = self.get_twaccount(follower)
                # TwAccount object
                if self.is_update_twitter(twaccount):
                    notification += '\t' + twaccount.screen_name + ' in Twitter\n'
                    isUpdated = True
                quora_account = self.get_qraccount(follower)
                if self.is_update_quora(quora_account):
                    notification += '\t' + quora_account.user_name + ' in Quora\n'
                    isUpdated = True
            if isUpdated:
                self.my_send_email(notification, accout.user.email)