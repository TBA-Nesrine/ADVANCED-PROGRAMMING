from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    publication_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name="books")
    reviews = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="books/", blank=True, null=True)
    
    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_rent = models.DateTimeField(auto_now_add=True)
    date_return = models.DateTimeField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    confirmed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} -> {self.book.title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title if self.book else 'General'}"

# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=100, unique=True)
    phone_contact = models.CharField(max_length=15, unique=True)
    user_address = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
