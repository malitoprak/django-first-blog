from django.urls import path, re_path
from blog.views import post_create, post_delete, post_list, post_update, sanatcilar, post_detail
# from .views import post_create, post_delete, post_list, post_update


urlpatterns = [
    re_path(r'^$', post_list, name='post-list'),
    re_path(r'^post-create/$', post_create, name='post-create'),
    re_path(r'^post-update/$', post_update),
    re_path(r'^post-delete/$', post_delete),
    re_path(r'^sanatcilar/(?P<sayi>[0-9a-zA-Z]+)/$', sanatcilar),
    re_path(r'^post-detail/(?P<pk>[0-9]+)/$', post_detail, name='post-detail')
]
