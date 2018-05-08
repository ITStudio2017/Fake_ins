from django.conf.urls import url, include
from .views import apiApplication
urlpatterns =[
	url(r'Application',apiApplication)
]