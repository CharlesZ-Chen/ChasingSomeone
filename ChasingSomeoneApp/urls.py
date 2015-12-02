from django.conf.urls import url
from .views import UserView, AuthView, FollowerView, TwStatusView, AccountView

urlpatterns = [
    url(r'^$',AuthView.user_login, name="user_login"),
    url(r'^login/$', AuthView.user_login, name="user_login"),
    url(r'^register/$', UserView.register, name='register'),
    url(r'^user_activate/(?P<user_pk>[0-9]+)/$', UserView.user_activate, name="user_activate"),
    url(r'^home/$', UserView.user_home, name='user_home'),
    url(r'^logout/$', AuthView.user_logout, name='user_logout'),

    url(r'^add_follower/$', FollowerView.add_follower, name="add_follower"),
    url(r'^delete_follower/$', FollowerView.delete_follower, name="delete_follower"),

    url(r'^verify_account/$', AccountView.http_verify_account, name="verify_account"),
    url(r'^save_account/$', AccountView.http_save_account, name="save_account"),
    url(r'^delete_account/$', AccountView.http_delete_account, name="delete_account"),

    # url(r'^add_follower_tw/$', TWAccountView.add_follower, name="add_follower_tw"),
    url(r'^get_status_tw/$', TwStatusView.get_status, name="get_status_tw"),
]

