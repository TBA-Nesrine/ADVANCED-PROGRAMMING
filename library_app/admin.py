from django.contrib import admin
from .models import Book, Genre, Order, User  

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Order)
admin.site.register(User)