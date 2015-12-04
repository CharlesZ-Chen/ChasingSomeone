from django.conf.urls import url
from .views import UserView, AuthView, FollowerView, AccountView, StatusView

urlpatterns = [
    url(r'^$', AuthView.user_login, name="user_login"),
    url(r'^login/$', AuthView.user_login, name="user_login"),
    url(r'^register/$', UserView.register, name='register'),
    url(r'^user_activate/(?P<user_pk>[0-9]+)/$', UserView.user_activate, name="user_activate"),
    url(r'^home/$', UserView.user_home, name='user_home'),
    url(r'^logout/$', AuthView.user_logout, name='user_logout'),

    url(r'browse_following/$', FollowerView.browse_following, name="browse_following"),
    url(r'^add_follower/$', FollowerView.add_follower, name="add_follower"),
    url(r'^delete_follower/$', FollowerView.delete_follower, name="delete_follower"),

    url(r'^verify_account/$', AccountView.http_verify_account, name="verify_account"),
    url(r'^save_account/$', AccountView.http_save_account, name="save_account"),
    url(r'^delete_account/$', AccountView.http_delete_account, name="delete_account"),

    url(r'refresh_status_site/$', StatusView.refresh_status_by_site, name="refresh_status_site"),
    url(r'refresh_status_flr/$', StatusView.refresh_status_by_flr, name='refresh_status_flr'),
]

