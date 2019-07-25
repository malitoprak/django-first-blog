from django.conf.urls import url
from .views import kullanici_takip_et_cikar, followed_or_followers_list
from django.urls import path, re_path

urlpatterns = [
    re_path(r'^takiplesme-sistemi/$', kullanici_takip_et_cikar, name='kullanici-takip-et-cikar'),
    re_path(r'^followed_or_followers_list/(?P<follow_type>[-\w]+)$', followed_or_followers_list, name='followed-or-followers-list')

]
