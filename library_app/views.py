# library_app/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.test import APIRequestFactory
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Genre

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate





# API imports
from .api.auth import *
from .api.admin import *
from .api.user import *



# =========================
# AUTH VIEWS
# =========================


# =========================
# AUTH VIEWS
# =========================

def signup_user(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        username = request.POST.get("account_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "library_app/signup.html")




def login_user(request):
    if request.method == "POST":
        username = request.POST.get("account_name")  # <-- match the form
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff or user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('user_home')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "library_app/login.html")


def logout_user(request):
    logout(request)
    return redirect("login")

# =========================
# ADMIN VIEWS
# =========================

@login_required
def admin_home(request):
    factory = APIRequestFactory()
    api_request = factory.get("/admin/dashboard/")
    api_request.user = request.user

    response = admin_dashboard(api_request)

    return render(request, "library_app/admin_home.html", {
        "most_read_books": response.data
    })


@login_required
def admin_books(request):
    factory = APIRequestFactory()
    api_request = factory.get("/admin/books/")
    api_request.user = request.user

    response = user_books(api_request)  # reuse books API
    return render(request, "library_app/admin_books.html", {
        "books": response.data
    })




from rest_framework.test import APIRequestFactory

@login_required
def admin_add_book_view(request):
    if request.method == "POST":
        factory = APIRequestFactory()

        api_request = factory.post(
            "/admin/books/add/",
            data={
                "title": request.POST.get("title"),
                "author": request.POST.get("author"),
                "quantity": request.POST.get("quantity"),
                "description": request.POST.get("description"),
                "genres": request.POST.getlist("genres"),
            },
            format="multipart"  # 👈 VERY IMPORTANT
        )

        # 👇 manually attach uploaded file
        api_request.FILES["image"] = request.FILES.get("image")

        api_request.user = request.user

        response = admin_add_book(api_request)

        print(response.data)

        return redirect("admin_books")

    return render(request, "library_app/admin_add_book.html", {
        "genres": Genre.objects.all()
    })




@login_required
def admin_delete_book_view(request, book_id):
    factory = APIRequestFactory()
    api_request = factory.delete(f"/admin/books/delete/{book_id}/")
    api_request.user = request.user

    admin_delete_book(api_request, book_id)
    return redirect("admin_books")


@login_required
def admin_orders_view(request):
    factory = APIRequestFactory()
    api_request = factory.get("/admin/orders/")
    api_request.user = request.user

    response = admin_orders(api_request)
    return render(request, "library_app/admin_orders.html", {
        "orders": response.data
    })


@login_required
def admin_reviews_view(request):
    reviews = Review.objects.select_related("user", "book").all()

    return render(request, "library_app/admin_reviews.html", {
        "reviews": reviews
    })

@login_required
def admin_delete_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    book = review.book
    review.delete()

    # Recalculate book rating
    if book:
        from django.db.models import Avg
        avg = Review.objects.filter(book=book).aggregate(Avg("rating"))["rating__avg"]
        book.reviews = round(avg, 1) if avg else None
        book.save()

    messages.success(request, "Review deleted successfully")
    return redirect("admin_reviews")


@login_required
def admin_users_view(request):
    factory = APIRequestFactory()
    api_request = factory.get("/admin/users/")
    api_request.user = request.user

    response = admin_users(api_request)
    return render(request, "library_app/admin_users.html", {
        "users": response.data
    })


from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
 # your custom User model

@login_required
def admin_add_user_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        User.objects.create_user(
            username=username,
            email=email,
            password="defaultpassword"
        )

        messages.success(request, "User added successfully")
        return redirect("admin_users")

    return render(request, "library_app/admin_add_user.html")


@login_required
def activate_user_view(request, user_id):
    factory = APIRequestFactory()
    api_request = factory.patch(f"/admin/users/activate/{user_id}/")
    api_request.user = request.user

    activate_user(api_request, user_id)
    return redirect("admin_users")


@login_required
def deactivate_user_view(request, user_id):
    factory = APIRequestFactory()
    api_request = factory.patch(f"/admin/users/deactivate/{user_id}/")
    api_request.user = request.user

    deactivate_user(api_request, user_id)
    return redirect("admin_users")




from rest_framework.test import APIRequestFactory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

@login_required
def admin_update_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.is_active = request.POST.get("is_active") == "True"  # ✅ fix here
        user.save()

        return redirect("admin_users")

    return render(request, "library_app/admin_edit_user.html", {
        "user": user
    })



@login_required
def admin_delete_user_view(request, user_id):
    factory = APIRequestFactory()
    api_request = factory.delete(f"/admin/users/delete/{user_id}/")
    api_request.user = request.user

    admin_delete_user(api_request, user_id)

    return redirect("admin_users")



@login_required
def admin_update_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        factory = APIRequestFactory()

        api_request = factory.patch(
            f"/admin/books/update/{book_id}/",
            data={
                "title": request.POST.get("title"),
                "author": request.POST.get("author"),
                "quantity": request.POST.get("quantity"),
                "description": request.POST.get("description"),
                "genres": request.POST.getlist("genres"),
            },
            format="multipart"
        )

        if request.FILES.get("image"):
            api_request.FILES["image"] = request.FILES.get("image")

        api_request.user = request.user

        admin_update_book(api_request, book_id)

        return redirect("admin_books")

    return render(request, "library_app/admin_edit_book.html", {
        "book": book,
        "genres": Genre.objects.all()
    })



# =========================
# USER VIEWS
# =========================

from django.db.models import Q
from .models import Genre

@login_required
def user_home(request):
    factory = APIRequestFactory()
    api_request = factory.get("/user/books/")
    api_request.user = request.user

    response = user_books(api_request)
    books = response.data  # list of dicts

    search_query = request.GET.get("q", "").lower()
    genre_filter = request.GET.get("genre", "All").lower()

    # SEARCH FILTER
    if search_query:
        books = [
            book for book in books
            if search_query in book["title"].lower()
            or search_query in book["author"].lower()
            or (book.get("description") and search_query in book["description"].lower())
        ]

    # GENRE FILTER
    if genre_filter != "all":
        filtered_books = []
        for book in books:
            # book["genres"] contains IDs
            book_genre_ids = book.get("genres", [])
            # get genre names
            book_genre_names = Genre.objects.filter(id__in=book_genre_ids).values_list('name', flat=True)
            if any(genre_filter == name.lower() for name in book_genre_names):
                filtered_books.append(book)
        books = filtered_books

    return render(request, "library_app/user_home.html", {
        "books": books,
        "genres": Genre.objects.all(),
        "search_query": request.GET.get("q", ""),
        "active_genre": request.GET.get("genre", "All"),
    })



@csrf_exempt
@login_required
def borrow_book(request):
    if request.method == "POST":
        factory = APIRequestFactory()
        api_request = factory.post("/user/borrow/", {
            "book_id": request.POST.get("book_id")
        })
        api_request.user = request.user

        user_borrow_book(api_request)
    return redirect("user_home")


@login_required
def user_mybag_view(request):
    factory = APIRequestFactory()
    api_request = factory.get("/user/mybag/")
    api_request.user = request.user

    response = user_mybag(api_request)
    return render(request, "library_app/user_mybag.html", {
        "orders": response.data
    })

@csrf_exempt
@login_required
def cancel_order(request):
    if request.method == "POST":
        factory = APIRequestFactory()
        api_request = factory.post("/user/cancel/", {
            "order_id": request.POST.get("order_id")
        })
        api_request.user = request.user

        user_cancel_order(api_request)

    return redirect("user_mybag")



from django.utils import timezone

@login_required
def return_book(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'accepted' and order.date_return is None:
        order.status = 'returned'
        order.date_return = timezone.now()
        order.save()
        messages.success(request, f"You returned '{order.book.title}' successfully!")
    else:
        messages.error(request, "This book cannot be returned.")

    return redirect("read_books")


@login_required
def reading_history(request):
    orders = Order.objects.filter(user=request.user, status='returned', date_return__isnull=False)
    return render(request, 'library_app/reading_history.html', {
        'returned_books': orders
    })

@login_required
def read_books(request):
    orders = Order.objects.filter(user=request.user, status='accepted', date_return__isnull=True)
    return render(request, 'library_app/read_books.html', {
        'read_books': orders
    })



# library_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from library_app.models import Book
from .api.user import add_review_for_user  # <-- import the function

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")

        # Call the function directly
        result = add_review_for_user(request.user, book_id, rating, comment)

        if result["success"]:
            messages.success(request, "Review added successfully!")
            return redirect("reading_history")
        else:
            messages.error(request, result.get("error", "Something went wrong"))

    return render(request, "library_app/add_review.html", {"book": book})




from django.shortcuts import render, redirect
from rest_framework.test import APIRequestFactory

from library_app.models import Book
from library_app.api.user import user_send_contact


def user_contactus(request):
    books = Book.objects.all()

    if request.method == "POST":
        factory = APIRequestFactory()
        api_request = factory.post(
            '/api/contact/',
            data=request.POST
        )
        api_request.user = request.user

        response = user_send_contact(api_request)

        if response.status_code == 200:
            return redirect('user_home')

    return render(
        request,
        'library_app/user_contactus.html',
        {'books': books}
    )



@login_required
def user_books_view(request):
    factory = APIRequestFactory()
    api_request = factory.get("/user/books/")
    api_request.user = request.user

    response = user_books(api_request)  # call your API function
    return render(request, "library_app/user_books.html", {
        "books": response.data
    })

@login_required
def user_note_view(request):
    factory = APIRequestFactory()
    api_request = factory.get("/user/read-books/")
    api_request.user = request.user

    response = user_read_books(api_request)

    return render(request, "library_app/user_note.html", {
        "read_books": response.data
    })


@login_required
def user_profile(request):
    return render(request, "library_app/user_profile.html")  # placeholder template

@login_required
def user_settings(request):
    return render(request, "library_app/user_settings.html")


"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from library_app.models import UserProfile

@login_required
def user_profile(request):
    # Get the profile if it exists, otherwise create a new one
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'library_app/user_profile.html', {"profile": profile})

@login_required
def change_profile(request):
    # Get or create the profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Update User model fields
        request.user.first_name = request.POST.get("full_name")
        request.user.email = request.POST.get("email")
        request.user.save()
        
        # Update UserProfile model fields
        profile.phone_contact = request.POST.get("phone_contact")
        profile.user_address = request.POST.get("user_address")
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile')  # redirect back to profile page

    return render(request, 'library_app/change_profile.html', {"profile": profile})


"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required
def user_profile(request):
    return render(request, "library_app/user_profile.html")


@login_required
def edit_profile(request):

    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")

        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("user_profile")

    return render(request, "library_app/edit_profile.html")


@login_required
def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            # VERY IMPORTANT:
            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully!")
            return redirect("user_profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "library_app/change_password.html", {
        "form": form
    })

from rest_framework.test import APIRequestFactory
from django.contrib.auth.decorators import login_required
from .api.user import *



@login_required
def user_profile_view(request):
    factory = APIRequestFactory()
    api_request = factory.get("/api/user/profile/")
    api_request.user = request.user

    response = get_user_profile(api_request)
    return render(request, "library_app/user_profile.html", {"profile": response.data})

from .api.user import update_user_profile


@login_required
def edit_profile_view(request):
    factory = APIRequestFactory()

    if request.method == "GET":
        api_request = factory.get("/api/user/profile/")
        api_request.user = request.user

        response = get_user_profile(api_request)
        return render(request, "library_app/edit_profile.html", {"profile": response.data})

    elif request.method == "POST":
        api_request = factory.put("/api/user/profile/update/", request.POST)
        api_request.user = request.user

        update_user_profile(api_request)
        return redirect("user_profile")

@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect("user_profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "library_app/change_password.html", {"form": form})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order

def admin_accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'accepted'
    order.save()
    messages.success(request, f"Order #{order.id} accepted!")
    return redirect('admin_orders')

def admin_refuse_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'refused'
    order.save()
    messages.error(request, f"Order #{order.id} refused.")
    return redirect('admin_orders')


from django.shortcuts import render
from rest_framework.test import APIRequestFactory

from library_app.api.user import user_book_details


def user_book_detail_view(request, book_id):

    factory = APIRequestFactory()
    api_request = factory.get(f'/api/books/{book_id}/')
    api_request.user = request.user

    response = user_book_details(api_request, book_id)

    data = response.data

    return render(
        request,
        'library_app/user_book_detail.html',
        {
            'book': data['book'],
            'reviews': data['reviews']
        }
    )



