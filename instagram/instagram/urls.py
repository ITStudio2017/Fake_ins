"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import django.views.static
from instagram.settings import BASE_DIR
import os
<<<<<<< HEAD
from ins_api.views import show_picture

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(.+)/$', show_picture),
=======
from users.models import User 
from rest_framework import routers, serializers, viewsets


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/',include('ins_api.urls')),
    url(r'^captcha/', include('captcha.urls')),

>>>>>>> e0cbbc4f480601bf6eddd5e926d5f3dfe39b610c
    url(r'static/(?P<path>.*)', django.views.static.serve, {'document_root': os.path.join(BASE_DIR, 'static')}),
]
