from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def show_picture(request, url):
    image_data = open('media/' + url, 'rb').read()
    return HttpResponse(image_data, content_type='image/png')
