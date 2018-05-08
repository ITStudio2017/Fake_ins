from django.shortcuts import render
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.db.models import Q
from .models import ApiApplicationer
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
				return render(request,'Application.html',{'message':'用户已存在'})
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



# Create your views here.
