from django.urls import path
from .auth import signup_api, login_api
from .admin import *
from .user import *
from django.urls import path
from . import views
from django.urls import path



urlpatterns = [



    path('review/<int:book_id>/', views.add_review_api, name='add_review_api'),


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
    # admin – late returns
    path('admin/late-returns/', admin_late_returns),
    path('admin/send-warning/', admin_send_return_warning),

    path("admin/orders/<int:order_id>/accept/",admin_accept_order,name="api_admin_accept_order",),
    path('admin/orders/<int:order_id>/refuse/', admin_refuse_order, name='api_admin_refuse_order'),

    #user
    path('user/books/', user_books),
    path('user/borrow/', user_borrow_book),
    path('user/mybag/', user_mybag),
    path('user/return/', user_return_book),
    path('user/feedback/', user_feedback),

    path('user/profile/', get_user_profile, name='user_profile_api'),   # GET
    path('user/profile/update/', update_user_profile, name='update_user_profile_api'),  # PUT
    path('user/change-password/', change_password, name='change_password_api'),  # PUT

    

]
