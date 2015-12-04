__author__ = 'charleszhuochen'
from django.db import models
from ChasingSomeoneApp.models.QrAccount import QrAccount


class QrStatus(models.Model):
    time_stamp = models.DateTimeField()
    url_profile_img = models.CharField(max_length=200)
    action_type = models.CharField(max_length=50)
    target = models.CharField(max_length=200)
    url_target = models.CharField(max_length=200)
    user_profile_name = models.CharField(max_length=50)
    qrAccount = models.ForeignKey(QrAccount)

    def __unicode__(self):
        return self.target
