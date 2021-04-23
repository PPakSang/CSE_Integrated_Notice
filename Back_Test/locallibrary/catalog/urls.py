from django.urls import path
from catalog import views
from .views import index
urlpatterns = [
    path('',index,name='index')
]