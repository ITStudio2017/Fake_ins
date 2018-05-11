from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from ins_api import views
urlpatterns =[
	url(r'Application/',views.apiApplication),
	url(r'user/detail/(?P<pk>[0-9]+)/$',views.UserDetail.as_view()),
	url(r'user/register/$',views.UserRegister.as_view()),
	url(r'user/register/activation/$',views.UserRegisterVerification.as_view()),
	url(r'user/login/$',views.UserToken.as_view()),

]