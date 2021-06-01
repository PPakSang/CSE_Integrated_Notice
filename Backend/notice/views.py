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
    tag1 = Uni_post.objects.filter(tags__name='멘토링')
    tag2 = Uni_post.objects.filter(tags__name='대학원')


    def get_context_data(self, **kwargs) :
        kwargs['tag1'] = self.tag1
        kwargs['tag2'] = self.tag2

        return super().get_context_data(**kwargs)

def mainview(request):
    # posts = Uni_post.objects.filter(post_origin='컴퓨터학부_전체')
    return render(request, 'notice/main.html')

def getPageInfo(request):
    # print(request.GET['origin'])
    post_origin = request.GET['origin']
    # print(request.GET['num'])
    page_num = int(request.GET['num'])
    # print(request.GET['tags'].split(','))
    tags = request.GET['tags'].split(',')
    posts = Uni_post.objects.filter(post_origin=post_origin,).order_by("-post_date")
    if request.GET['tags'].split(',') == ['']: #해당 origin post 전체 호출
        posts = posts
    else: #태그가 넘어왔을시
        for tag in tags:
            posts = posts.filter(tags__name = tag)
    
    # print(posts.count())
    
    posts_len = int(posts.count())//11+1
    posts = posts[10*(page_num-1):10*page_num]
    posts = render_to_string('notice/post_list.html',{"posts":posts})
    tags = Tag.objects.filter(origin=post_origin).order_by("-name")
    tags = serializers.serialize("json", tags)
    # print(tags)
    context = {
        "posts":posts,
        "posts_len":posts_len,
        "tags": tags
    }
    context = json.dumps(context)
    return HttpResponse(context)
    

def detailview(request, url):
    qs = request.GET.urlencode()
    url = f"{url}?{qs}"
    contents = Uni_post.objects.filter(post_url=url)[0]
    title = contents.post_title
    author = contents.post_author
    date = contents.post_date
    attch = contents.attachment_info
    contents = contents.post_contents
    return render(request, "notice/detail_view.html", {
        "title": title,
        "author" : author,
        "date" : date,
        "attch" : attch,
        "contents" : contents,
    })
