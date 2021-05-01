from django.urls import path
from .views import BoardListView,BoardCreateView

urlpatterns=[
    path('',BoardListView.as_view(),name='boardlist'),  #.as_view 클래스형 뷰를 함수형 뷰로 바꿈 / 인자는 대부분 함수형이 들어감
    path('add/',BoardCreateView.as_view(),name='add'),
]