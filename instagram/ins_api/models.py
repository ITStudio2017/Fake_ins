from django.db import models
from users.models import User

class Posts(models.Model):
	"""动态"""
	user = models.ForeignKey(User,verbose_name="用户")
	introduction = models.CharField(max_length=150,default="",verbose_name="动态")
	Pub_time = models.DateTimeField(auto_now_add=True,verbose_name="发表时间")
	likes_num = models.PositiveIntegerField(default=0,verbose_name="点赞数")
	com_num = models.PositiveIntegerField(default=0,verbose_name="评论数")

class Photos(models.Model):
	"""动态的图片"""
	post = models.ForeignKey(Posts,verbose_name="动态")
	photo = models.CharField(max_length=100,default="",verbose_name="图片")

class Comments(models.Model):
	"""动态评论"""
	user = models.ForeignKey(User,verbose_name="用户")
	post = models.ForeignKey(Posts,verbose_name="动态")
	content = models.CharField(max_length=80,blank=False)
	Pub_time = models.DateTimeField(auto_now_add=True,verbose_name="发表时间")
		
	
class UsersActive(models.Model):
		"""用于储存注册时的激活码和忘记密码发送的验证码"""
		STATUS_CHOICES=(
			(1,"注册"),
			(2,"忘记")
			)
		user = models.ForeignKey(User,verbose_name="用户")
		status = models.PositiveIntegerField(choices=STATUS_CHOICES,default=1,verbose_name="状态")
		code = models.CharField(max_length=10,default="",verbose_name="验证码")

class LikesLink(models.Model):
	"""点赞关联信息"""
	user = models.ForeignKey(User,verbose_name="用户")
	post = models.ForeignKey(Posts,verbose_name="动态")

class PostsLink(models.Model):
	"""收藏关联信息"""
	user = models.ForeignKey(User,verbose_name="用户")
	post = models.ForeignKey(Posts,verbose_name="动态")

class FollowsLink(models.Model):
	"""用于储存用户关注关联信息"""
	From = models.ForeignKey(User,related_name='from+',verbose_name="关注者")
	To = models.ForeignKey(User,verbose_name="被关注者",related_name='to')

class ApiList(models.Model):
	appId = models.CharField(max_length=20,default="")
	appKey = models.CharField(max_length=100,default="")
	publicKey = models.CharField(max_length=160,default="")
	privateKey = models.CharField(max_length=160,default="")
		
		
class ApiApplicationer(models.Model):
	email = models.EmailField()
	name = models.CharField(max_length=10)
	permission = models.BooleanField(default=False)
	
		
		
		

				


