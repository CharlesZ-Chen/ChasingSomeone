__author__ = 'charleszhuochen'
from django.db import models
from ChasingSomeoneApp.models.TwFollower import TwFollower


class TwStatus(models.Model):

    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    text = models.CharField(max_length=500)
    img_url = models.ImageField(blank=True)
    lang = models.CharField(max_length=20, default='en')

    twFollower = models.ForeignKey(TwFollower)

    def __unicode__(self):
        return self.text
