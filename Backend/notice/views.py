from django.http.request import QueryDict
from .models import Tag,Uni_post
from django.shortcuts import render
from django.views import generic
from django.db import models
from typing import Any, Dict


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

def test_view(request):
    if request.method == 'POST':
        a = request.POST
        b = {'key':1}
        c = []
        
        a = a.getlist(key = 'object')
        

        return render(request,'test.html',{'a' : a})

    return render(request,'test.html')