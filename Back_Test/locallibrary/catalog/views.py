from django.shortcuts import render
from catalog.models import Author,Book,BookInstance,Genre
from django.views import generic
# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    num_instances_available=BookInstance.objects.filter(status__exact='a').count()

    num_specific_genre=Genre.objects.filter(name__icontains='Western').count()

    num_authors=Author.objects.count()

    num_visit=request.session.get('num_visit',0) 

    request.session['num_visit']=num_visit+1
    
    context={
        'num_books': num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_specific_genre':num_specific_genre,
        'num_visit':num_visit,
    }

    return render(request,'index.html',context=context)


class BookListView(generic.ListView):
    model=Book
    paginate_by=2
    
    


class BookDetailView(generic.DetailView):
    model=Book


class AuthorListView(generic.ListView):
    model=Author

class AuthorDetailView(generic.DetailView):
    model=Author
    

#DetailView 작동 원리

# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book': book})