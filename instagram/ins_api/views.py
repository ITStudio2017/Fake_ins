from django.shortcuts import render
from django.http import HttpResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.db.models import Q
from .models import ApiApplicationer
from rest_framework import serializers, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from django.http import Http404
from .serializers import UserSerializer
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import EmailMessage
from .models import UsersActive
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt



def apiApplication(request):
	if request.method == 'POST':
		email = request.POST['email']
		name = request.POST['name']
		hashkey = request.POST['captcha_0']
		captcha = request.POST['captcha_1']
		realCaptcha = CaptchaStore.objects.get(hashkey=hashkey)
		if (realCaptcha.response == captcha.lower()):
			try:
				user = ApiApplicationer.objects.get(email=email)
				return render(request,'Application.html',{'message':'请不要重复申请。'})
			except:
				ApiApplicationer.objects.create(email=email,name=name)
				return render(request,'Application.html',{'message':'申请成功，请等待结果'})
		return render(request,'Application.html',{'message':'验证码错误'})

	hashkey = CaptchaStore.generate_key()
	image_url = captcha_image_url(hashkey)
	content = {
	'image_url':image_url,
	'hashkey':hashkey,
	}
	return render(request,'Application.html',{'hashkey':hashkey,
											  'image_url':image_url})


class UserDetail(APIView):
	permission_classes = (IsAuthenticated,)
	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			raise Http404

	def get(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = UserSerializer(user)
		return Response(serializer.data)
		


class UserRegister(APIView):
	def post(self, request, format=None):
		data = request.data
		username = data['username']
		email = data['email']
		password = data['password']
		password2 = data['password2']
		nickname = data['nickname']
		try:
			User.objects.get(username=username)
			return Response({'errors':'账号名重复'})
		except:
			try:
				User.objects.get(email=email)
				return Response({'errors':'邮箱已注册'})
			except:
				if password != password2:
					return Response({'errors':'两次密码不一致'})
				password = make_password(password)
				user = User.objects.create(username=username,email=email,password=password,nickname=nickname)
				hashkey = CaptchaStore.generate_key()
				captcha = CaptchaStore.objects.get(hashkey=hashkey)
				code = captcha.challenge
				UsersActive.objects.create(user=user,hashkey=hashkey,code=code,status=1)
				sendemail = EmailMessage('验证码','您好，您的验证码是' + code,"alex_noreply@163.com",[email,])
				sendemail.send()
				return Response({'status':'验证码已发送'})



class UserRegisterVerification(APIView):
	def post(self, request, format=None):
		try:
			data = request.data
			code = data['code']
			hashkey = data['hashkey']
			captcha = UsersActive.objects.get(hashkey=hashkey)
			captcha1 = CaptchaStore.objects.get(hashkey=hashkey)
			user = User.objects.get(username=captcha.user)
			if (captcha1.response == code.lower()):
				user.is_active = True
				user.save()
				captcha.delete()
				captcha1.delete()
				return Response({'status':'激活成功'})
			return Response({'status':'验证码错误！'})
		except:
			return Response({'status':'未知错误'})


class UserToken(APIView):
	def post(self, request, format=None,):
		return Response({'status':'登录成功！'})



		


def show_picture(request, url):
	image_data = open('media/' + url, 'rb').read()
	return HttpResponse(image_data, content_type='image/png')
