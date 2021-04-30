from django.shortcuts import render
from catalog.models import Author,Book,BookInstance,Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# class MyView(LoginRequiredMixin,View):
#     login_url='/login/'
#     redirect_field_name='redirect_to'

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

#     return render(request, 'catalog/book_detail.h tml', context={'book': book})



#LoginRequiredMixin 이 view에 접근하려면 login이 필요하며 안되어있으면 ~~해라 

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginate_by=10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')