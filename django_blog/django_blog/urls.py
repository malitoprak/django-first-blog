"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from blog.views import iletisim, deneme, deneme_ajax, deneme_ajax2


urlpatterns = [
    re_path(r'^deneme/$', deneme, name='deneme'),
    re_path(r'^deneme/ajax$', deneme_ajax, name='deneme-ajax'),
    re_path(r'^deneme/ajax-2$', deneme_ajax2, name='deneme-ajax2'),
    path('admin/', admin.site.urls),
    re_path(r'^posts/', include('blog.urls')),
    re_path(r'^auths/', include('auths.urls')),
    re_path(r'^following/', include('following.urls')),
    re_path(r'^iletisim/', iletisim, name='iletisim'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
