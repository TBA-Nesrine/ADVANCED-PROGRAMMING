"""from django.urls import path, include

urlpatterns = [
    path('api/', include('library_app.api.urls')),
]"""

from django.urls import path
from .views import user_home, borrow_book

urlpatterns = [
    path('user/home/', user_home, name='user_home'),
    path('user/borrow/', borrow_book, name='user_borrow_book'),
    
]
