from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard', views.library_dash,name='dashboard'),
    path('', views.book_list, name='library_list'),
    path('book/<int:pk>/', views.book_detail, name='library_detail'),
    path('book/new/', views.book_create, name='library_create'),
    path('book/<int:pk>/edit/', views.book_update, name='library_update'),
    # Add URLs for LibraryTransaction
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
# ---------------------------------------------------ajax----------------------------------------------------------------------
    path('ffetch_books/', views.fetch_books, name='fetch_books'),
# ---------------------------------------------------ajax----------------------------------------------------------------------


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 