__author__ = 'charleszhuochen'
from django.db import models
from ChasingSomeoneApp.models.UserProfile import User

class Follower(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name
