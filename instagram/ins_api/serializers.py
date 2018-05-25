from rest_framework import serializers
from users.models import User
from .models import Posts, Photos, Comments, LikesLink

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username',
				  'nickname', 'gender', 'birthday',
				  'following_num', 'followed_num',
				  'following_num', 'profile_picture',
				  'introduction','address')

class BriefUser(object):
	"""docstring for BriefUser"""
	def __init__(self, user_id, username, gender, birthday, following_num, followed_num, profile_picture, is_guanzhu):
		self.user_id = user_id
		self.username = username
		self.gender = gender
		self.birthday = birthday
		self.following_num = following_num
		self.followed_num = followed_num
		self.profile_picture = profile_picture
		self.is_guanzhu = is_guanzhu

class BriefUserSerializer(serializers.Serializer):
	user_id = serializers.IntegerField()
	username = serializers.CharField()
	gender = serializers.IntegerField()
	birthday = serializers.CharField()
	following_num = serializers.IntegerField()
	followed_num = serializers.IntegerField()
	profile_picture = serializers.ImageField()
	is_guanzhu = serializers.BooleanField()

class BriefPost(object):
	"""docstring for ClassName"""
	def __init__(self, username, introduction, Pub_time, likes_num, com_num, profile_picture, photo_0, is_dianzan, is_shoucang, post_id, user_id):
		self.username = username
		self.profile_picture = profile_picture
		self.introduction = introduction
		self.Pub_time = Pub_time
		self.likes_num = likes_num
		self.com_num = com_num
		self.photo_0 = photo_0
		self.is_dianzan = is_dianzan
		self.is_shoucang = is_shoucang
		self.post_id = post_id
		self.user_id = user_id

class BriefPostSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=15)
	introduction = serializers.CharField(max_length=150)
	Pub_time = serializers.DateTimeField()
	profile_picture = serializers.ImageField()
	likes_num = serializers.IntegerField()
	com_num = serializers.IntegerField()
	photo_0 = serializers.ImageField()
	is_shoucang = serializers.BooleanField()
	is_dianzan = serializers.BooleanField()
	post_id = serializers.IntegerField()
	user_id = serializers.IntegerField()
		

class PostSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Posts
		fields = ('id', 'user', 'introduction',
				  'Pub_time', 'likes_num',
				  'com_num','photo_0')

class PhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Photos
		fields = ('id', 'post', 'photo')



class CommentSerializer(serializers.ModelSerializer):
	"""docstring for CommentSerializer"""
	class Meta():
		model = Comments
		fields = ('id','user','post','content','Pub_time')

class LikesLinkSerializer(serializers.ModelSerializer):
	class Meta:
		model = LikesLink
		fields = ('id','user','post','time')

class BriefLikesLink(object):
	"""docstring for BriefLikesLink"""
	def __init__(self, username, user_id, post_id, introduction, photo_0, profile_picture, time):
		self.username = username
		self.user_id = user_id
		self.post_id = post_id
		self.introduction = introduction
		self.photo_0 = photo_0
		self.profile_picture = profile_picture
		self.time = time

class BriefLikesLinkSerializer(serializers.Serializer):
	"""点赞"""
	username = serializers.CharField()
	user_id = serializers.IntegerField()
	post_id = serializers.IntegerField()
	introduction = serializers.CharField()
	photo_0 = serializers.ImageField()
	profile_picture = serializers.ImageField()
	time = serializers.DateTimeField()


		