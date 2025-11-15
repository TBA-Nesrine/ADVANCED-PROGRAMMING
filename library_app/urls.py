from django.urls import path
from . import views

urlpatterns = [
    # ---------- User Auth ----------
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # ---------- Custom Admin Dashboard ----------
    path('dashboard/home/', views.admin_home, name='admin_home'),

    # Users
    # Admin Users
path('dashboard/users/', views.admin_users, name='admin_users'),
path('dashboard/users/add/', views.admin_add_user, name='admin_add_user'),
path('dashboard/users/activate/<str:ref>/', views.activate_user, name='activate_user'),
path('dashboard/users/deactivate/<str:ref>/', views.deactivate_user, name='deactivate_user'),


    # Books
    path('dashboard/books/', views.admin_books, name='admin_books'),
    path('dashboard/books/add/', views.admin_add_book, name='admin_add_book'),
    path('dashboard/books/delete/<int:book_id>/', views.admin_delete_book, name='admin_delete_book'),

    # Orders, Reviews, Returns
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/reviews/', views.admin_reviews, name='admin_reviews'),
    path('dashboard/returns/', views.admin_returns, name='admin_returns'),

    # ---------- User Views ----------
    path('', views.user_home, name='home'),
    path('books/', views.user_books, name='user_books'),
    path('mybag/', views.user_mybag, name='user_mybag'),
    path('contactus/', views.user_contactus, name='user_contactus'),
    path('note/', views.user_note, name='user_note'),

]


