from os import name
from django.conf.urls import url
from django.urls import path
from .views import *



urlpatterns = [
    path('', mainview, name='main'),
    path('getpageinfo/', getPageInfo, name='getpageinfo'),
    path('detailview/<path:url>', detailview, name="detailview"),
    path('start/', startCrawling, name="crawling"),
]