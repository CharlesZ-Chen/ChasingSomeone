from django.contrib import admin
from ChasingSomeoneApp.models.UserProfile import UserProfile
from ChasingSomeoneApp.models.Follower import Follower
from ChasingSomeoneApp.models.TwAccount import TwAccount
from ChasingSomeoneApp.models.TwStatus import TwStatus
from ChasingSomeoneApp.models.QrAccount import QrAccount
from ChasingSomeoneApp.models.QrStatus import QrStatus
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TwAccount)
admin.site.register(TwStatus)
admin.site.register(Follower)
admin.site.register(QrAccount)
admin.site.register(QrStatus)
