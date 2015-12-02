__author__ = 'charleszhuochen'
from django.db import models
from ChasingSomeoneApp.models.Follower import Follower


class TwAccount(models.Model):
    act_id = models.CharField(max_length=45)
    screen_name = models.CharField(max_length=45)
    # follower specified id, using for distinguish follower.
    both_id = models.CharField(max_length=45, help_text=" Specifies the ID or screen name of the user", blank=True)
    profile_img = models.ImageField(blank=True)

    follower = models.OneToOneField(Follower, primary_key=True)

    def __unicode__(self):
        return self.screen_name
