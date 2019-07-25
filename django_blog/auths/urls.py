from django.urls import path, include, re_path
from .views import RegisterForm, register, user_login, user_logout, user_profile, user_settings, user_about, \
    user_password_change

urlpatterns = [
    re_path(r'^register/$', view=register, name='register'),
    re_path(r'^login/$', view=user_login, name='user_login'),
    re_path(r'^logout/$', view=user_logout, name='user_logout'),
    re_path(r'^settings/$', view=user_settings, name='user-settings'),
    re_path(r'^password-change/$', view=user_password_change, name='user-password-change'),
    re_path(r'^(?P<username>[-\w]+)/$', view=user_profile, name='user-profile'),
    re_path(r'^(?P<username>[-\w]+)/about$', view=user_about, name='user-about')

]
