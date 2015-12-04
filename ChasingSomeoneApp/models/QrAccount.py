__author__ = 'charleszhuochen'
from django.db import models
from ChasingSomeoneApp.models.Follower import Follower


class QrAccount(models.Model):
    user_name = models.CharField(max_length=45)
    profile_img = models.CharField(max_length=200, blank=True, null=True)

    follower = models.OneToOneField(Follower, primary_key=True)

    def __unicode__(self):
        return self.user_name
