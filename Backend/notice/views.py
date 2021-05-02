from os import name
from django.db import models
from django.shortcuts import render
from django.views import generic
from .models import Tag,Uni_post
from typing import Any, Dict




# Create your views here.

class Notice_listview(generic.ListView):
    model=Uni_post
    template_name='notice/notice_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for i in range(1,4):
            context['tag'+str(i)]=Uni_post.objects.filter(tag__name='멘토링'+str(i))

        return context
    

        

        



    