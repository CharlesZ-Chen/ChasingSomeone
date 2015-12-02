__author__ = 'charleszhuochen'
from django.db import models
from ChasingSomeoneApp.models.UserProfile import User

class Follower(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User)

    # def save(self, *args, **kwargs):
    #     self.name = kwargs['name']
    #     self.user = kwargs['user']
    #     self.birthday = kwargs['birthday']
    #     super(Follower, self).save(*args, **kwargs)
