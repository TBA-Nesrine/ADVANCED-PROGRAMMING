# library_app/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.test import APIRequestFactory
from django.shortcuts import render, redirect
from django.contrib import messages

# API imports
from .api.auth import signup_api, login_api
from .api.admin import (
    admin_dashboard,
    admin_add_book,
    admin_delete_book,
    admin_orders,
    admin_reviews,
    admin_users,
    admin_add_user,
    activate_user,
    deactivate_user,
)
from .api.user import (
    user_books,
    user_borrow_book,
    user_mybag,
    user_return_book,
    user_feedback,
)

from .models import Genre


# =========================
# AUTH VIEWS
# =========================


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

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


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

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


@login_required
def admin_add_book_view(request):
    if request.method == "POST":
        factory = APIRequestFactory()
        api_request = factory.post("/admin/books/add/", {
            "title": request.POST.get("title"),
            "author": request.POST.get("author"),
            "quantity": request.POST.get("quantity"),
            "description": request.POST.get("description"),
        })
        api_request.user = request.user

        admin_add_book(api_request)
        return redirect("admin_books")

    return render(request, "library_app/admin_add_book.html")


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
    factory = APIRequestFactory()
    api_request = factory.get("/admin/reviews/")
    api_request.user = request.user

    response = admin_reviews(api_request)
    return render(request, "library_app/admin_reviews.html", {
        "reviews": response.data
    })


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
from library_app.models import UserProfile

def admin_users_view(request):
    users = UserProfile.objects.all()
    return render(request, "library_app/admin_users.html", {"users": users})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from library_app.models import UserProfile  # your custom User model

@login_required
def admin_add_user_view(request):
    if request.method == "POST":
        # Get form data safely, default to empty string to avoid None
        full_name = request.POST.get("user_name", "").strip()
        email = request.POST.get("email", "").strip()
        reference_id = request.POST.get("reference_id", "").strip()
        phone_contact = request.POST.get("phone_contact", "").strip()
        user_address = request.POST.get("user_address", "").strip()

        if not full_name or not email:
            return render(request, "library_app/admin_add_user.html", {"error": "Name and email are required."})

        # Create Django user
        user = User.objects.create(username=full_name, email=email)
        user.set_password("defaultpassword")  # you can later ask for a password
        user.save()

        # Create custom profile
        UserProfile.objects.create(
            user=user,
            reference_id=reference_id,
            phone_contact=phone_contact,
            user_address=user_address,
            active=True
        )

        messages.success(request, "User added successfully")
        return redirect("admin_users")

    return render(request, "library_app/admin_add_user.html")


@login_required
def activate_user_view(request, ref):
    factory = APIRequestFactory()
    api_request = factory.patch(f"/admin/users/activate/{ref}/")
    api_request.user = request.user

    activate_user(api_request, ref)
    return redirect("admin_users")


@login_required
def deactivate_user_view(request, ref):
    factory = APIRequestFactory()
    api_request = factory.patch(f"/admin/users/deactivate/{ref}/")
    api_request.user = request.user

    deactivate_user(api_request, ref)
    return redirect("admin_users")


# =========================
# USER VIEWS
# =========================

@login_required
def user_home(request):
    factory = APIRequestFactory()
    api_request = factory.get("/user/books/")
    api_request.user = request.user

    response = user_books(api_request)

    return render(request, "library_app/user_home.html", {
        "books": response.data,
        "genres": Genre.objects.all()
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
def return_book(request):
    if request.method == "POST":
        factory = APIRequestFactory()
        api_request = factory.post("/user/return/", {
            "order_id": request.POST.get("order_id")
        })
        api_request.user = request.user

        user_return_book(api_request)

    return redirect("user_mybag")


@login_required
def user_contactus(request):
    if request.method == "POST":
        factory = APIRequestFactory()
        api_request = factory.post("/user/feedback/", {
            "book_id": request.POST.get("book_id"),
            "feedback": request.POST.get("feedback"),
        })
        api_request.user = request.user

        user_feedback(api_request)
        return redirect("user_contactus")

    return render(request, "library_app/user_contactus.html")

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
    # Example: fetch user notes from API
    factory = APIRequestFactory()
    api_request = factory.get("/user/notes/")
    api_request.user = request.user

    response = user_feedback(api_request)  # assuming notes use feedback API
    return render(request, "library_app/user_note.html", {
        "notes": response.data
    })

@login_required
def user_profile(request):
    return render(request, "library_app/user_profile.html")  # placeholder template

@login_required
def user_settings(request):
    return render(request, "library_app/user_settings.html")





