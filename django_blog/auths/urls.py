from django.urls import path, include, re_path
from .views import RegisterForm

urlpatterns = [
    re_path(r'^register/$', view=register, name='register'),
]
