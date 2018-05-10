from django.conf.urls import url, include
from .views import apiApplication
from rest_framework.urlpatterns import format_suffix_patterns
from ins_api import views
urlpatterns =[
	url(r'Application/',apiApplication),
	url(r'user/detail/(?P<pk>[0-9]+)/$',views.UserDetail.as_view()),
	url(r'user/$',views.UserApi.as_view()),

]