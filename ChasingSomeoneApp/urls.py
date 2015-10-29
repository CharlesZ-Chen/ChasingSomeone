from django.conf.urls import include, url
from .views import UserViews, AuthViews

urlpatterns = [
    url(r'^$', AuthViews.index, name="index"),
    url(r'^login/$', AuthViews.login, name="login"),
    url(r'^register/$', UserViews.register, name='register'),
]
