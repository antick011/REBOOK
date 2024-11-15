from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import views module

urlpatterns = [
    path('', views.home, name='home'),  # Home page view
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/new/', views.BookCreateView.as_view(), name='book-create'),
    path('signup/', views.signup, name='signup'),  # Sign-up view
    path('sell/', views.sell_book, name='sell_book'),  # Sell book view
    path('buy/<int:book_id>/', views.buy_book, name='buy_book'),
    path('login/', views.login_view, name='login'),  # Login view
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('buy/<int:book_id>/payment/', views.payment, name='payment'),
    path('buy/<int:book_id>/confirmation/', views.buy_confirmation, name='buy_confirmation'),
]
