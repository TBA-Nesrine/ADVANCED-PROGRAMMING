# library_app/views.py
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from rest_framework.test import APIRequestFactory
from .api.user import user_books, user_borrow_book  # your API functions
from .models import Genre
from django.views.decorators.csrf import csrf_exempt

# -------------------------------
# User Home Page
# -------------------------------

def user_home(request):
    # Collect filter from form
    search_query = request.GET.get('q', '')
    active_genre = request.GET.get('genre', 'All')

    # Call API internally
    factory = APIRequestFactory()
    api_request = factory.get('/user/books/')
    api_request.user = request.user
    response = user_books(api_request)
    books = response.data

    # Filter results in Python (optional)
    if active_genre != 'All':
        books = [b for b in books if any(g['name'] == active_genre for g in b.get('genres', []))]

    if search_query:
        books = [b for b in books if search_query.lower() in b['title'].lower() or search_query.lower() in b['author'].lower()]

    return render(request, 'library_app/user_home.html', {
        'books': books,
        'genres': Genre.objects.all(),
        'active_genre': active_genre,
        'search_query': search_query
    })

# -------------------------------
# Borrow Book
# -------------------------------
@csrf_exempt
def borrow_book(request):
    """
    Handles borrowing a book from user_home.
    Calls the API internally.
    """
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        factory = APIRequestFactory()
        api_request = factory.post('/user/borrow/', {'book_id': book_id}, format='json')
        api_request.user = request.user  # attach logged-in user

        response = user_borrow_book(api_request)
        # Optional: handle success or error messages here

        return redirect('user_home')

    return redirect('user_home')

