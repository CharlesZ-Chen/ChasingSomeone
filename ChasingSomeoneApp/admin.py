from django.contrib import admin
from ChasingSomeoneApp.models.UserProfile import UserProfile
from ChasingSomeoneApp.models.TwFollower import TwFollower
from ChasingSomeoneApp.models.TwStatus import TwStatus
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TwFollower)
admin.site.register(TwStatus)
