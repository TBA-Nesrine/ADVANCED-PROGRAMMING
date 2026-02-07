from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Order, Review

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email"
        ]

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'



from rest_framework import serializers
from library_app.models import Order

class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user_id",
            "username",
            "book_title",
            "quantity",
            "date_rent",
            "date_return",
            "status",
        ]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth.models import User



from django.contrib.auth.models import User
from rest_framework import serializers

