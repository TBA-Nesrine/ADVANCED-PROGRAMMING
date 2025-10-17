from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    account_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.account_name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    publication_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name="books")  # 👈 creates join table
    reviews = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_rent = models.DateTimeField(auto_now_add=True)
    date_return = models.DateTimeField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.account_name} -> {self.book.title}"