from django.urls import path, re_path
from blog.views import post_create, post_delete, post_list, post_update, sanatcilar, post_detail, add_comment, add_or_remove_favorite
# from .views import post_create, post_delete, post_list, post_update


urlpatterns = [
    re_path(r'^$', post_list, name='post-list'),
    re_path(r'^post-create/$', post_create, name='post-create'),
    re_path(r'^post-update/(?P<slug>[-\w]+)/$', post_update, name='post-update'),
    re_path(r'^post-delete/(?P<slug>[-\w]+)/$', post_delete, name='post-delete'),
    # re_path(r'^post-delete/(?P<slug>[0-9]+)/$', post_delete, name='post-delete'),
    re_path(r'^sanatcilar/(?P<slug>[-\w]+)/$', sanatcilar),
    re_path(r'^post-detail/(?P<slug>[-\w]+)/$', post_detail, name='post-detail'),
    re_path(r'^add-comment/(?P<slug>[-\w]+)/$', add_comment, name='add-comment'),
    re_path(r'^add-remove-favorite/(?P<slug>[-\w]+)/$', add_or_remove_favorite, name='add-remove-favorite')
]
