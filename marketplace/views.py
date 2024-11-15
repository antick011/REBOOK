from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Book
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import BookForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})  # Make sure this path is correct


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful sign up
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'marketplace/book_form.html'
    
    # Redirect to 'home' after successful book creation
    success_url = reverse_lazy('home')  # Ensure this matches the URL pattern name

    def form_valid(self, form):
        form.instance.seller = self.request.user  # Set the seller to the current user
        return super().form_valid(form)


@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'marketplace/buy_confirmation.html', {'book': book})


@login_required
def sell_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'marketplace/sell_book.html', {'form': form}) 


def home(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'marketplace/home.html', {'books': books, 'query': query})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home after sign-up
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class BookListView(ListView):
    model = Book
    template_name = 'marketplace/book_list.html'
    context_object_name = 'books'
    ordering = ['-created_at']

class BookDetailView(DetailView):
    model = Book
    template_name = 'marketplace/book_detail.html'
    context_object_name = 'book'

@method_decorator(login_required, name='dispatch')
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'marketplace/book_form.html'
    
    success_url = reverse_lazy('home')  # Redirect to home after creation

    def form_valid(self, form):
        form.instance.seller = self.request.user  # Set the seller to the currently logged-in user
        return super().form_valid(form)

       

def book_list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 10)  # Show 10 books per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'marketplace/book_list.html',)

def buy_confirmation(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'marketplace/buy_confirmation.html', {'book': book})

def payment(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # Add any additional logic for the payment page (e.g., payment gateway, form handling, etc.)
    return render(request, 'marketplace/payment.html', {'book': book})


