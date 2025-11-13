# this is the class that intereacts with the databse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q
from .models import Book, Order, Review
from django.utils import timezone

# ---------------- AUTH ----------------
def signup_user(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('account_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('signup')
        user = User.objects.create_user(username=username, email=email, password=password, first_name=full_name)
        messages.success(request, 'Account created successfully!')
        return redirect('login')
    return render(request, 'library_app/signup.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('account_name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            return redirect('home')
        messages.error(request, 'Invalid credentials')
        return redirect('login')
    return render(request, 'library_app/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# ---------------- ADMIN VIEWS ----------------
@login_required
def admin_home(request):
    most_read_books = Book.objects.annotate(read_count=Count('order')).order_by('-read_count')[:5]
    return render(request, 'library_app/admin_home.html', {'most_read_books': most_read_books})

@login_required
def admin_users(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'library_app/admin_users.html', {'users': users})

@login_required
def admin_books(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'library_app/admin_books.html', {'books': books})

@login_required
def admin_add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        quantity = int(request.POST.get('quantity', 0))
        description = request.POST.get('description')
        book = Book.objects.create(title=title, author=author, quantity=quantity, description=description)
        messages.success(request, 'Book added successfully!')
        return redirect('admin_books')
    return render(request, 'library_app/admin_add_book.html')

@login_required
def admin_delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('admin_books')

@login_required
def admin_orders(request):
    orders = Order.objects.select_related('user', 'book').all()
    return render(request, 'library_app/admin_orders.html', {'orders': orders})

@login_required
def admin_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'library_app/admin_reviews.html', {'reviews': reviews})

@login_required
def admin_returns(request):
    returns = Order.objects.filter(date_return__isnull=False)
    return render(request, 'library_app/admin_returns.html', {'returns': returns})

# ---------------- USER VIEWS ----------------
@login_required
def user_home(request):
    most_read_books = Book.objects.annotate(read_count=Count('order')).order_by('-read_count')[:5]
    return render(request, 'library_app/user_home.html', {'most_read_books': most_read_books})

@login_required
def user_books(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    if request.method == 'POST':
        book_id = int(request.POST.get('book_id'))
        book = get_object_or_404(Book, id=book_id)
        if book.quantity > 0:
            Order.objects.create(user=request.user, book=book, quantity=1)
            book.quantity -= 1
            book.save()
            messages.success(request, 'Book added to your bag')
        else:
            messages.error(request, 'Book not available')
        return redirect('user_books')
    return render(request, 'library_app/user_books.html', {'books': books})

@login_required
def user_mybag(request):
    orders = Order.objects.filter(user=request.user, date_return__isnull=True)
    if request.method == 'POST':
        order_id = int(request.POST.get('order_id'))
        order = get_object_or_404(Order, id=order_id)
        order.date_return = timezone.now()
        order.save()
        book = order.book
        book.quantity += order.quantity
        book.save()
        messages.success(request, 'Book returned successfully')
        return redirect('user_mybag')
    return render(request, 'library_app/user_mybag.html', {'orders': orders})

@login_required
def user_contactus(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id) if book_id else None
        Review.objects.create(user=request.user, book=book, feedback=feedback)
        messages.success(request, 'Feedback sent successfully')
        return redirect('user_contactus')
    books = Book.objects.all()
    return render(request, 'library_app/user_contactus.html', {'books': books})

@login_required
def user_note(request):
    read_books = Order.objects.filter(user=request.user, date_return__isnull=False)
    return render(request, 'library_app/user_note.html', {'read_books': read_books})
