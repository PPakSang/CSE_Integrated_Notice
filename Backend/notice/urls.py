from django.urls import path
from .views import *


urlpatterns=[
    path('',Notice_listview.as_view(),name='list')
]