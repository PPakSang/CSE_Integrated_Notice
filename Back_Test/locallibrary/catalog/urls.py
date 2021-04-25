from django.urls import path
from catalog import views
from .views import index
urlpatterns = [
    path('',index,name='index'),
    path('books/',views.BookListView.as_view(),name="books"),
    path('books/<int:pk>/',views.BookDetailView.as_view(),name='book-detail'),
    path('authors/',views.AuthorListView.as_view(),name='Authors'),
    path('authors/<int:pk>/',views.AuthorDetailView.as_view(),name='Author-detail'),
]