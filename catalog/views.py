from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#This is to declare a view that works on a form.
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

#from catalog.forms import RenewedBookForm

from catalog.forms import RenewBookModelForm


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author




#This is a class-based view that gives a user permission.
class MyBookView(PermissionRequiredMixin, View):
    permission_required=("catalog.can_mark_returned", "catalog.change_book")


#This is the class_based view for the book model
class BookListView(generic.ListView):
    model=Book
    context_object_name= "book_list" #the object_name can be anything
    queryset=Book.objects.filter(title__icontains="marriage")[:3] #Get 3 books with the title marriage.
    template_name="book_list.html"


#This is the class_based view for the bookdetail url 
class BookDetailView(generic.DetailView):
    model=Book


#This class is a generic class-based view that list books on loan to current users
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginate_by=10

    def get_queryset(self):
        return(
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )

# Create your views here.

"""View function for the home page of site"""

def index(request):
    
    #Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    #Available books (status="a")
    num_instances_available=BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors=Author.objects.count()
    
    #Number of visits to this view, as counted in the session varaible
    num_visits= request.session.get("num_visits", 0)
    request.session["num_visits"]=num_visits + 1


    context={
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian"""
    book_instance=get_object_or_404(BookInstance, pk=pk)

    #if this is a POST request then process the Form data
    if request.method=='POST':

        #Create a form instance and populate it with the data from the request (binding)
        form=RenewBookModelForm(request.POST)

        #Check if the form is valid
        if form.is_valid():
            #process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back=form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('/'))
    # if this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date=datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={"due_back": proposed_renewal_date})

    context={
        'form': form,
        'book_instance': book_instance,
    }     

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model=Author
    fields=['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial={'date_of_death': "01/01/2000"}
    permission_required="catalog.add_author"


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model=Author
    #It is not recommended to use the __all__ dunder as it become a security issue when new fields are added.
    fields='__all__'
    permission_required="catalog.change_author"


class AuthorDelete(PermissionError, DeleteView):
    model=Author
    success_url= reverse_lazy('authors')
    permission_required="catalog.delete_author"


    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )