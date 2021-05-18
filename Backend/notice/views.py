from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponse
from .models import Tag,Uni_post
from django.shortcuts import redirect, render
from django.views import generic
from django.db import models
from typing import Any, Dict
from django.views.decorators.csrf import csrf_exempt
import json
from collections import OrderedDict
from django.core import serializers

# Create your views here.
class Notice_listview(generic.ListView):
    model = Uni_post
    template_name='notice/notice_list.html'

    tag1 = Uni_post.objects.filter(tag__name = '교직')
    tag2 = Uni_post.objects.filter(tag__name = '휴학')


    def get_context_data(self, **kwargs) :

        kwargs['tag1'] = self.tag1
        kwargs['tag2'] = self.tag2

        return super().get_context_data(**kwargs)

    
generic.DetailView

QueryDict
import sys
@csrf_exempt
def test_view(request):
    if request.method =='POST':
        tags = request.POST['tags'].split(',')
        
        
        post = Uni_post.objects.all()
        for i in tags :
            post = post.filter(tag__name = i)
     
        
        
        post = serializers.serialize('json',post)
        return HttpResponse(post)

    return render(request,'test.html')


