from django.conf.urls import url
from django.urls import path
from .views import *



urlpatterns = [
    path('', Notice_listview.as_view(), name='list'),
    path('test/', test_view, name='test'),
]