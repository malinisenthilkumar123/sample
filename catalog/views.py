from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Book, Author, BookInstance, Genre

# 📌 Home Page View
def index(request):
    """View function for the home page of the site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # Pass all data to the template
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context)

# 📌 Book List View
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'

# 📌 Book Detail View
class BookDetailView(generic.DetailView):
    model = Book

# 📌 Author List View
class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    context_object_name = 'authors'

# 📌 Author Detail View (with visit tracking)
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'
    
    def get_context_data(self, **kwargs):
        # Get the existing context
        context = super().get_context_data(**kwargs)
        
        # Get session data safely
        num_visits = self.request.session.get('num_visits', 0)
        
        # Store updated visit count in session
        self.request.session['num_visits'] = num_visits + 1
        
        # Add visit count to the context
        context['num_visits'] = num_visits + 1

        return context


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from catalog.models import BookInstance

class LoanedBooksListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user, status='o').order_by('due_back')

