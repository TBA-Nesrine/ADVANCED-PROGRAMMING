from django.contrib import admin
from .models import Book, Genre, Review,Order
from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genres')
    search_fields = ('title', 'author', 'genres__name')  # include genre in search
    list_filter = ('genres',)
    filter_horizontal = ('genres',)  # allows selecting multiple genres easily

    # Helper method to display genres as a comma-separated string
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Genres'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'quantity', 'date_rent', 'date_return', 'confirmed')
    list_filter = ('confirmed', 'date_rent')
    search_fields = ('user__username', 'book__title')
    actions = ['confirm_order']

    def confirm_order(self, request, queryset):
        updated = queryset.update(confirmed=True)
        self.message_user(request, f"{updated} order(s) confirmed successfully.")
    confirm_order.short_description = "Confirm selected orders"

admin.site.register(Order, OrderAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Review)

