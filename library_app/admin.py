from django.contrib import admin
from .models import Book, Genre, Review

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genres')
    search_fields = ('title', 'author', 'genres__name')  # include genre in search
    list_filter = ('genres',)
    filter_horizontal = ('genres',)  # allows selecting multiple genres easily

    # Helper method to display genres as a comma-separated string
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Genres'

admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Review)
