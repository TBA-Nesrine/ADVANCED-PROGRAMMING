from django.urls import path
from .auth import signup_api, login_api
from .admin import *
from .user import *


urlpatterns = [
    #auth
    path('auth/signup/', signup_api),
    path('auth/login/', login_api),
    
    #admin
    path('admin/dashboard/', admin_dashboard),
    path('admin/books/add/', admin_add_book),
    path('admin/books/delete/<int:book_id>/', admin_delete_book),
    path('admin/books/<int:book_id>/update/', admin_update_book),
    path('admin/orders/', admin_orders),
    path('admin/orders/<int:order_id>/confirm/', confirm_order),
    path('admin/reviews/', admin_reviews),
    path('admin/users/', admin_users),
    path('admin/users/<int:user_id>/update/', admin_update_user),
    path('admin/users/activate/<str:ref>/', activate_user),
    path('admin/users/deactivate/<str:ref>/', deactivate_user),
    
    #user
    path('user/books/', user_books),
    path('user/borrow/', user_borrow_book),
    path('user/mybag/', user_mybag),
    path('user/return/', user_return_book),
    path('user/feedback/', user_feedback),

    
    

]
