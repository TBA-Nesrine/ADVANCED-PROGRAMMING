from django.shortcuts import redirect
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [

    # =====================
    # ROOT REDIRECT
    # =====================
    path('', lambda request: redirect('login')),

    # =====================
    # API ROUTES
    # =====================
    path('api/', include('library_app.api.urls')),

    # =====================
    # AUTH (TEMPLATES)
    # =====================
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # =====================
    # ADMIN DASHBOARD
    # =====================
    path('dashboard/home/', views.admin_home, name='admin_home'),
    path('dashboard/books/', views.admin_books, name='admin_books'),
    path('dashboard/books/add/', views.admin_add_book_view, name='admin_add_book'),
    path('dashboard/books/delete/<int:book_id>/', views.admin_delete_book_view, name='admin_delete_book'),
    path('dashboard/orders/', views.admin_orders_view, name='admin_orders'),
    path('dashboard/reviews/', views.admin_reviews_view, name='admin_reviews'),

    path('dashboard/users/', views.admin_users_view, name='admin_users'),
    path('dashboard/users/add/', views.admin_add_user_view, name='admin_add_user'),

    # 🔥 FIXED → USING ID
    path('dashboard/users/activate/<int:user_id>/', views.activate_user_view, name='activate_user'),
    path('dashboard/users/deactivate/<int:user_id>/', views.deactivate_user_view, name='deactivate_user'),

    # =====================
    # USER
    # =====================
    path('user/home/', views.user_home, name='user_home'),
    path('user/books/', views.user_books_view, name='user_books'),
    path('user/borrow/', views.borrow_book, name='user_borrow_book'),
    path('user/mybag/', views.user_mybag_view, name='user_mybag'),
    path('user/return/', views.return_book, name='user_return_book'),
    path('user/notes/', views.user_note_view, name='user_note'),
    path('user/contact/', views.user_contactus, name='user_contactus'),
    path('user/settings/', views.user_settings, name='user_settings'),
    path('user/profile/', views.user_profile_view, name='user_profile'),
    path('user/profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('user/change-password/', views.change_password_view, name='change_password'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )