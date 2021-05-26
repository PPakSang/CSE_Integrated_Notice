from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from .models import Tag, Uni_post
from django.views import generic
from django.db import models
from typing import Any, Dict
import json
from collections import OrderedDict
from django.core import serializers

# Create your views here.
class Notice_listview(generic.ListView):
    model = Uni_post
    template_name = 'notice/notice_list.html'
    tag1 = Uni_post.objects.filter(tags__name = '교직')
    tag2 = Uni_post.objects.filter(tags__name = '휴학')


    def get_context_data(self, **kwargs) :

        kwargs['tag1'] = self.tag1
        kwargs['tag2'] = self.tag2

        return super().get_context_data(**kwargs)

def mainview(request):
    posts = Uni_post.objects.filter(post_origin = '컴퓨터학부_글솝')
    return render(request,'notice/main.html')

def getPageInfo(request):
    print(request.GET['origin'])
    post_origin = request.GET['origin']
    posts = Uni_post.objects.filter(post_origin = post_origin).order_by()[:5]
    posts_len = len(posts)
    posts = render_to_string('notice/post_list.html',{"posts":posts})
    print(posts)
    context = {
        "posts":posts,
        "posts_len":posts_len
    }
    context = json.dumps(context)
    return HttpResponse(context)
