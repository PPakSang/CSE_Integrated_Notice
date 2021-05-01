from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#view는 CRUD 가 기본 Create,Read,Update,Delete
#함수형 view 가 있고, generic view 가 있다

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Board
from django.urls import reverse_lazy

class BoardListView(ListView):
    model=Board

class BoardCreateView(CreateView):
    model=Board
    fields=['board_name','post']
    success_url=reverse_lazy('boardlist')
    template_name_suffix='test'