from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','username','nickname','gender','birthday','following_num','followed_num','following_num','profile_picture')
			


