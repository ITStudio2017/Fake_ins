from django.shortcuts import render
from django.http import HttpResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.db.models import Q
from rest_framework import serializers, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from django.http import Http404
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import rsa
from .serializers import UserSerializer, PostSerializer, PhotoSerializer, CommentSerializer, LikesLinkSerializer, BriefPostSerializer, BriefPost
from .models import ApiApplicationer, Posts, UsersActive, Keys, Photos, FollowsLink, LikesLink
import hashlib 
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, mixins
import time
from users.utils import EmailActivationTokenGenerator, send_activation_email
from users.signals import user_activated, user_registered


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

class ShortPost(APIView):
	def get(self, request, pk, format=None):
		photoList = Photos.objects.filter(post=pk).order_by('-time')
		post = Posts.objects.get(pk=pk)
		user = User.objects.get(id=post.user.id)
		briefPost = BriefPost(username=user.username,introduction=post.introduction, Pub_time=post.Pub_time, photo=photoList[0].photo)
		serializer = BriefPostSerializer(briefPost)
		return Response(serializer.data)

		
class UserDetail(APIView):
	permission_classes = (IsAuthenticated,)
	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			raise Http404

	def get(self, request, pk, format=None):
		"""10"""
		user = self.get_object(pk)
		serializer = UserSerializer(user)
		return Response(serializer.data)

	def put(self, request, format=None):
		"""11"""
		data = request.data
		try:
			user = User.objects.get(id=request.user.id)
			user.profile_picture = data['profile_picture']
			user.username = data['username']			
			user.nickname = data['nickname']
			user.gender = data['gender']
			user.birthday = data['birthday']
			if User.objects.filter(username=user.username):
				return Response({'status':'AccountError'})
			user.save()
			return Response({'status':'Success'})
		except:
			return Response({'status':'UnknownError'})

class PhotoList(APIView):
	def get(self, request):
		try:
			postid = request.GET['postid']
			photoList = Photos.objects.filter(post=postid).order_by('-time')
			serializer = PhotoSerializer(photoList, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})


		


class UserRegister(APIView):
	"""2"""
	def post(self, request, format=None):
		data = request.data
		username = data['username']
		email = data['email']
		password = data['password']
		nickname = data['nickname']
		try:
			User.objects.get(username=username)
			return Response({'status':'AccountError'})
		except:
			try:
				User.objects.get(email=email)
				return Response({'status':'EmailError'})
			except:
				password = make_password(password)
				try:
					user = User.objects.create(username=username,email=email,password=password,nickname=nickname)
					opts = {
					'user': user,
					'request': request,
					'from_email': None,
					'email_template': 'users/activation_email.html',
					'subject_template': 'users/activation_email_subject.html',
					'html_email_template': None,
					}
					send_activation_email(**opts)
					user_registered.send(sender=user.__class__, request=request, user=user)
					return Response({'status':'Success'})
				except:
					return Response({'status':'UnknownError'})


class Accounts(APIView):
	"""3"""
	def post(self, request, format=None):
		data = request.data
		try:
			if User.objects.filter(username=data['account']) or User.objects.filter(email=data['account']):
				return Response({'status':'Exist'})
			else:
				return Response({'status':'NotExist'})
		except:
			return Response({'status':'UnknownError'})
		

# class UserRegisterVerification(APIView):
# 	def post(self, request, format=None):
# 		try:
# 			data = request.data
# 			code = data['code']
# 			hashkey = data['hashkey']
# 			captcha = UsersActive.objects.get(hashkey=hashkey)
# 			captcha1 = CaptchaStore.objects.get(hashkey=hashkey)
# 			user = User.objects.get(username=captcha.user)
# 			if (captcha1.response == code.lower()):
# 				user.is_active = True
# 				user.save()
# 				captcha.delete()
# 				captcha1.delete()
# 				return Response({'status':'Success'})
# 			return Response({'status':'Failure'})
# 		except:
# 			return Response({'status':'UnknownError'})





class UserToken(APIView):
	"""1"""
	def post(self, request, format=None,):
		data = request.data
		try:
			login_type = data['login_type']
		except:
			return Response({'status':'UnknownError'})
		if login_type == 'email':
			try:
				email = data['email']
				user = User.objects.get(email=email)
			except:
				return Response({'status':'EmailError'})
		else:
			try:
				username = data['username']
				user = User.objects.get(username=username)
			except:
				return Response({'status':'UserNameError'})
		password = data['password']
		if not user.is_active:
			return Response({'status':'NotActive'})
		if user.check_password(password):
			try:
				token = Token.objects.get(user=user)
				token.delete()
			except:
				pass
			token = Token.objects.create(user=user)
			serializer = UserSerializer(user)
			return Response({'status':'Success','Authorization':'Token '+ token.key, "result":[serializer.data]})
		else:
			return Response({'status':'PasswordError'})

class PostDetail(APIView):
	"""22"""
	def get(self, request, pk, format=None):
		try:
			post = Posts.objects.get(pk=pk)
			serializer = PostSerializer(post)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})

		

class PostsAPI(generics.ListCreateAPIView):
	"""7"""
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		user = request.user
		userlist = [user.id]
		likeList = FollowsLink.objects.filter(From = user)
		for like in likeList:
			userlist.append(like.To.id)
		userlist = list(set(userlist))
		postList = Posts.objects.filter(user__in=userlist).order_by('-Pub_time')
		serializer = PostSerializer(postList, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		try:
			data = request.data
			photo_num = int(data['photo_num'])
			post = Posts.objects.create(user=request.user, introduction=data['introduction'])
			for i in range(photo_num):
				photo = Photos.objects.create(photo=data['photo_'+ str(i)],post=post)
				photo.save()
			post.save()
			return Response({'status':'Success'})
		except:
			return Response({'status':'UnknownError'})

	def put(self, request,format=None):
		"""7+"""
		data = request.data
		try:
			pk = request.data['pk']
			post = Posts.objects.get(pk=pk)
			post.introduction = data['introduction']
			post.seve()
			return Response({'status':'Success'})
		except:
			return Response({'status':'Failure'})

	def delete(self, request, format=None):
		"""23"""
		try:
			pk = request.GET['pk']
			user = request.user
			post = Posts.objects.get(pk=pk,user=user)
			post.delete()
			return Response({'status':'Success'})
		except:
			return Response({'status':'UnknownError'})

class PostList(mixins.ListModelMixin,
			   mixins.CreateModelMixin,
			   generics.GenericAPIView):
	queryset = Posts.objects.all()
	serializer_class = PostSerializer
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	# def list(self, request):
	# 	serializer = PostSerializer(self.get_queryset(),many=True)
	# 	return Response(serializer.data)

	
	def get_queryset(self):
		user = self.request.user
		userlist = [user.id]
		likeList = FollowsLink.objects.filter(From = user)
		for like in likeList:
			userlist.append(like.To.id)
		userlist = list(set(userlist))
		postList = Posts.objects.filter(user__in=userlist).order_by('-Pub_time')
		return postList


	
		

class UserPost(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request, pk, format=None):
		try:
			postList = Posts.objects.filter(user=pk)
			serializer = PostSerializer(pohotList, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})

		

class PasswordForget(APIView):
	"""5"""
	def get(self, request,format=None):
		try:
			email = request.GET['email']
		except:
			return Response({'status':'UnknownError'})
		try:
			user = User.objects.get(email=email)
		except:
			return Response({'status':'NotExist'})
		hashkey = CaptchaStore.generate_key()
		captcha = CaptchaStore.objects.get(hashkey=hashkey)
		code = captcha.challenge
		UsersActive.objects.create(user=user,hashkey=hashkey,code=code,status=2)
		sendemail = EmailMessage('验证码','您好，您的验证码是' + code,"alex_noreply@163.com",[email,])
		sendemail.send()
		return Response({'status':'Success','hashkey':hashkey})

	def post(self, request, format=None):
		data = request.data
		try:
			captcha = data['captcha']
			hashkey = data['hashkey']
			password = data['password']
			password2 = data['password2']
			response = CaptchaStore.objects.get(hashkey=hashkey).response
			if response == captcha and password == password2:
				user.password = make_password(password)
				return Response({'status':'Success'})
			else:
				return Response({'status':'Failure'})
		except:
			return Response({'status':'UnknownError'})




class Comments(APIView):
	"""24"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			post = request.GET['post']
			commentList = Comments.objects.filter(post=post)
			serializer = CommentSerializer(commentList, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})

	def post(self, request,post, format=None):
		data = request.data
		try:
			comment = Comments.objects.create(user=request.user, post=post, content=data['content'])
			comment.save()
			return Response({'status':'Success'})
		except:
			return Response({'status':'Failure'})

	def delete(self, request, post=None, format=None):
		data = request.data
		try:
			comment = Comments.objects.get(post=post, user=request.user)
			comment.delete()
			return Response({'status':'Success'})
		except:
			return Response({'status':'Failure'})


class Search(APIView):
	"""8"""
	def post(self, request, format=None):
		data = request.data
		try:
			searchType = data['searchType']
			if searchType == 'user':
				keyword = data['keyword']
				user = User.objects.filter(Q(email__contains=keyword) | Q(username__contains=keyword)).order_by('-followed_num')
				serializer = UserSerializer(user, many=True)
			if searchType == 'post':
				keyword = data['keyword']
				postList = Posts.objects.filter(introduction__contains=keyword).order_by('-Pub_time')
				serializer = PostSerializer(postList, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})

class FollowPost(APIView):
	def get(self, request, format=None):
		"""9"""
		data = request.data
		user = request.user
		try:
			followList = FollowsLink.objects.filter(From=user)
			userList = []
			for follow in followList:
				userList.append(follow.To.id)
			postList = Posts.objects.filter(user__in=userList).order_by('-Pub_time')
			serializer = PostSerializer(postList, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})

class LikeList(APIView):
	def get(self, request, format=None):
		"""13"""
		try:
			likeList = LikesLink.objects.filter(user=request.user)
			postIDList = []
			for like in likeList:
				postIDList.append(like.post.id)
			postList = Posts.objects.filter(id__in=postIDList).order_by('-Pub_time')
			serializer = PostSerializer(postList, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})
		

class Like(APIView):
	def get(self, request, format=None):
		"""12"""
		user = request.user
		try:
			likeList = LikesLink.objects.filter(user=user)
			postList = []
			for like in likeList:
				postList.append(like.post)
			posts = Posts.objects.filter(id__in=pohotList)
			serializer = PostSerializer(posts)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})

	def post(self, request, format=None):
		"""20,21"""
		data = request.data
		try:
			if LikesLink.objects.filter(post=data['post_id'],user=request.user):
				like = LikesLink.objects.filter(post=data['post_id'],user=request.user)
				like.delete()
				post = Posts.objects.get(id=data['post_id'])
				post.likeNumDreacase()
				post.save()
			else:
				post_id = data['post_id']
				like = LikesLink.objects.create(post=post_id,user=request.user)
				like.save()
				post = Posts.objects.get(id=data['post_id'])
				post.likeNumIncrease()
		except:
			return Response({'status':'UnknownError'})



class FollowPerson(APIView):
	"""14"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		user = request.user
		try:
			followList = FollowsLink.objects.filter(From=user)
			ToList = []
			for follow in followList:
				ToList.append(follow.To.id)
			userList = User.objects.filter(id__in=ToList)
			serializer = UserSerializer(userList, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})

		
class ToPerson(APIView):
	"""15"""
	def post(self, request, format=None):
		user = request.user
		try:
			followList = FollowsLink.objects.filter(To=user)
			FromList = []
			for follow in followList:
				FromList.append(follow.From.id)
			userList = User.objects.filter(id__in=FromList)
			serializer = UserSerializer(userlist, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})

		
class FollowMessage(APIView):
	"""17"""
	def post(self, request, format=None):
		try:
			followList = FollowsLink.objects.filter(From=request.user)
			ToList = []
			for follow in followList:
				ToList.append(follow.To.id)
			like = LikesLink.objects.filter(user__in=ToList).order_by('-time')
			serializer = LikesLinkSerializer(like, many=True)
			return Response(serializer.data)
		except:
			return Response({'status':'UnknownError'})



class Follow(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		"""18,19"""
		user = request.user
		try:
			data = request.data
			To = User.objects.get(pk=data['pk'])
			if FollowsLink.objects.filter(From=user,To=To):
				follow = FollowsLink.objects.filter(From=user,To=To)
				follow.delete()
				return Response({'status':'Success'})
			else:
				follow = FollowsLink.objects.create(From=user, To=To)
				follow.save()
				return Response({'status':'Success'})
		except:
			return Response({'status':'UnknownError'})

		
				



class PublicKey(APIView):
	def get(self, request, format=None):
		(pubkey, privkey) = rsa.newkeys(1024)
		pubkey = pubkey.save_pkcs1()
		privkey = privkey.save_pkcs1()
		key = Keys.objects.create(publicKey=pubkey,privateKey=privkey)
		key.save()
		return Response({'pubkey':pubkey})




class Test(APIView):
	def get(self, request, format=None):
		timestamp = time.time()
		timestamp = str(timestamp)
		return Response({'timestamp':timestamp})
		# user = request.user
		# serializer = UserSerializer(user)
		# return Response(serializer.data)

	def post(self, request, format=None):
		# a = ""
		# for i in request.data:
		# 	a += i
		# 	a += request.data[i]
		# print(a)
		# b = hashlib.md5(a.encode(encoding='utf-8'))
		# c = hashlib.md5(("a123b456").encode(encoding='gb2312'))
		# if b.hexdigest() == c.hexdigest():
		# 	print("True")
		# else:
		# 	print("False")
		# print(b.hexdigest())
		# print(c.hexdigest())
		print(request.path)
		if request.path == "/api/test/":
			print("True")
		else:
			print("False")
		return Response({'status':'OK'})

		



		




def show_picture(request, url):
	image_data = open('media/' + url, 'rb').read()
	return HttpResponse(image_data, content_type='image/png')
