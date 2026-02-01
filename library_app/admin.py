from django.contrib import admin
from .models import Book, Genre, Review, Order


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genres')
    search_fields = ('title', 'author', 'genres__name')
    list_filter = ('genres',)
    filter_horizontal = ('genres',)

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Genres'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'book',
        'quantity',
        'status',
        'date_rent',
        'date_return',
    )
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
    actions = ['accept_orders']

    def accept_orders(self, request, queryset):
        accepted_count = 0

        for order in queryset:
            if order.status == 'waiting':
                book = order.book
                if book.quantity >= order.quantity:
                    book.quantity -= order.quantity
                    book.save()

                    order.status = 'accepted'
                    order.save()
                    accepted_count += 1

        self.message_user(
            request,
            f"{accepted_count} order(s) accepted successfully."
        )

    accept_orders.short_description = "Accept selected orders"


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Review)
