from rest_framework import serializers
from users.models import User
from .models import Posts, Photos, Comments, LikesLink

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username',
				  'nickname', 'gender', 'birthday',
				  'following_num', 'followed_num',
				  'following_num', 'profile_picture')
			

class BriefPost(object):
	"""docstring for ClassName"""
	def __init__(self, username, introduction, Pub_time, photo):
		self.username = username
		self.introduction = introduction
		self.Pub_time = Pub_time
		self.photo = photo
		

class BriefPostSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=15)
	introduction = serializers.CharField(max_length=150)
	Pub_time = serializers.DateTimeField()
	photo = serializers.ImageField()
		

class PostSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Posts
		fields = ('id', 'user', 'introduction',
				  'Pub_time', 'likes_num',
				  'com_num',)

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
			
						
		
	
			
		