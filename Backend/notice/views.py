from django.db import models
from django.shortcuts import render
from django.views import generic
from .models import Tag,Uni_post

# Create your views here.

class Notice_listview(generic.ListView):
    model=Uni_post
    template_name='notice/notice_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data()

        return super().get_context_data(**kwargs)



    