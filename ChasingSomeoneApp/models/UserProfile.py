__author__ = 'charleszhuochen'
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    #link UserProfile to django.contrib.auth User
    user = models.OneToOneField(User)

    #addinational attributes created here

    #Override the __unicode__() method to return user's email address
    def __unicode__(self):
        return self.user.email

