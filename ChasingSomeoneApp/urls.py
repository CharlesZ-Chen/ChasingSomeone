from django.conf.urls import url
from .views import UserView, AuthView, TWFollowerView, TwStatusView

urlpatterns = [
    url(r'^$',AuthView.user_login, name="user_login"),
    url(r'^login/$', AuthView.user_login, name="user_login"),
    url(r'^register/$', UserView.register, name='register'),
    url(r'^home/$', UserView.user_home, name='user_home'),
    url(r'^logout/$', AuthView.user_logout, name='user_logout'),
    url(r'^add_follower_tw/$', TWFollowerView.add_follower, name="add_follower_tw"),
    url(r'^get_status_tw/$', TwStatusView.get_status, name="get_status_tw"),
    # url(r'^user_activate?(?P<user_pk>[.]*)$', UserView.user_activate, name="user_activate")
    url(r'^user_activate/(?P<user_pk>[0-9]+)/$', UserView.user_activate, name="user_activate")
]

