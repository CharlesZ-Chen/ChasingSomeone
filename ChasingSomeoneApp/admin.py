from django.contrib import admin
from ChasingSomeoneApp.models.UserProfile import UserProfile
from ChasingSomeoneApp.models.TwAccount import TwAccount
from ChasingSomeoneApp.models.TwStatus import TwStatus
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TwAccount)
admin.site.register(TwStatus)
