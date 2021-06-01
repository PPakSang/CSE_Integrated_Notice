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

    def get_context_data(self, **kwargs):
        kwargs['tag1'] = self.tag1
        kwargs['tag2'] = self.tag2

        return super().get_context_data(**kwargs)


def mainview(request):
    return render(request, 'notice/main.html')


def getPageInfo(request):
    page_num = int(request.GET['num'])
    keyword = request.GET.get("search", None)
    # 검색 시
    if (keyword):
        posts = Uni_post.objects.filter(post_title__icontains=keyword).order_by("-post_date")
    else:
        post_origin = request.GET['origin']
        tags = request.GET['tags'].split(',')
        posts = Uni_post.objects.filter(post_origin=post_origin).order_by("-post_date")
        if request.GET['tags'].split(',') == ['']:  # 해당 origin post 전체 호출
            posts = posts
        else: # 태그가 넘어왔을시
            for tag in tags:
                posts = posts.filter(tags__name=tag)
        tags = Tag.objects.filter(origin=post_origin).order_by("-name")
        tags = serializers.serialize("json", tags)

    posts_len = int(posts.count())//11+1
    posts = posts[10*(page_num-1):10*page_num]
    posts = render_to_string('notice/post_list.html', {"posts": posts})

    context = {
        "posts": posts,
        "posts_len": posts_len,
        "tags": tags if not keyword else ""
    }
    context = json.dumps(context, ensure_ascii=False)
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
        "author": author,
        "date": date,
        "attch": attch,
        "contents": contents,
    })