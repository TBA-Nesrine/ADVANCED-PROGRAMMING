from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Count
from django.contrib.auth.models import User
from ..models import Book, Order, Review
from ..serializers import BookSerializer, OrderSerializer, ReviewSerializer,UserSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from ..serializers import BookSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_admin_books(request):
    q = request.GET.get("q", "")

    books = Book.objects.all()

    if q:
        books = books.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q)
        )

    return Response(BookSerializer(books, many=True).data)



@api_view(['GET'])
def admin_dashboard(request):
    books = Book.objects.annotate(read_count=Count('order')).order_by('-read_count')[:5]
    return Response(BookSerializer(books, many=True).data)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def admin_add_book(request):
    serializer = BookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)

@api_view(['DELETE'])
def admin_delete_book(request, book_id):
    Book.objects.filter(id=book_id).delete()
    return Response({"message": "deleted"})

@api_view(['PATCH'])
def admin_update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    serializer = BookSerializer(book, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_orders(request):
    orders = Order.objects.filter(status='waiting').select_related('user', 'book')
    return Response(OrderSerializer(orders, many=True).data)

from django.shortcuts import get_object_or_404


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def admin_accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status != "waiting":
        return Response(
            {"error": "Order already processed"},
            status=400
        )

    book = order.book

    if book.quantity < order.quantity:
        return Response(
            {"error": "Not enough stock"},
            status=400
        )

    book.quantity -= order.quantity
    book.save()

    order.status = "accepted"
    order.accepted_at = timezone.now()
    order.save()

    return Response({"message": "Order accepted"})

# api/admin.py
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from ..models import Order



@api_view(["PATCH"])
def admin_refuse_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()  # delete the order if refused
    return Response({"success": True})


@api_view(['PATCH'])
def confirm_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    if order.confirmed:
        return Response({"message": "Order already confirmed"}, status=200)

    order.confirmed = True
    order.save()

    return Response({"message": f"Order {order.id} confirmed successfully"})

@api_view(['GET'])
def admin_reviews(request):
    return Response(ReviewSerializer(Review.objects.all(), many=True).data)

# api/admin.py
from django.contrib.auth.models import User
from rest_framework.response import Response

from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User

def api_admin_users(request):  # renamed to avoid collisions
    q = request.GET.get("q", "")  # get search query

    users = User.objects.all()

    if q:  # filter by username or email
        users = users.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q)
        )

    data = []
    for u in users:
        data.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_active": u.is_active
        })
    return Response(data)



@api_view(['PATCH'])
def admin_update_user(request, user_id):
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['PATCH'])
def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return Response({"message": "User activated"})

@api_view(['PATCH'])
def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return Response({"message": "User deactivated"})


@api_view(['POST'])
def admin_add_user(request):
    """
    API endpoint for admin to add a new user.
    """
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User


@api_view(['DELETE'])
def admin_delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    return Response({"message": "User deleted successfully"})


# api/admin.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from ..models import Order


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_late_returns(request):
    one_month_ago = timezone.now() - timedelta(minutes=5)

    orders = Order.objects.filter(
        status__in=['accepted'],
        accepted_at__lte=one_month_ago
    ).select_related('user', 'book')

    return Response([
        {
            "id": o.id,
            "username": o.user.username,
            "email": o.user.email,
            "book": o.book.title,
            "accepted_at": o.accepted_at,
        }
        for o in orders
    ])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_send_return_warning(request):
    order_ids = request.data.get('order_ids', [])

    orders = Order.objects.filter(id__in=order_ids)

    for order in orders:
        send_mail(
            subject="⚠️ Book Return Reminder",
            message=(
                f"Hello {order.user.first_name or order.user.username},\n\n"
                f"You borrowed '{order.book.title}' on {order.date_rent.date()}.\n"
                "Please return it as soon as possible.\n\n"
                "Library Administration"
            ),
            from_email="library@example.com",
            recipient_list=[order.user.email],
            fail_silently=False,
        )

    return Response({"message": "Warnings sent"})

#genre ------------------------------------------------------------------------------------------------------------
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models.functions import Lower
from ..models import Genre

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_add_genre(request):
    name = request.data.get("name", "").strip()

    if not name:
        return Response(
            {"error": "Genre name is required"},
            status=400
        )

    #Case-insensitive check
    if Genre.objects.filter(name__iexact=name).exists():
        return Response(
            {"error": "Can't add genre because it already exists"},
            status=400
        )

    genre = Genre.objects.create(name=name)
    return Response(
        {"message": "Genre added successfully", "id": genre.id, "name": genre.name},
        status=201
    )

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from ..models import Genre
from django.db.models import Count

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_genres_list(request):
    genres = Genre.objects.annotate(nb_books=Count('books')).order_by('name')
    data = [
        {"id": g.id, "name": g.name, "nb_books": g.nb_books}
        for g in genres
    ]
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_genre(request, genre_id):
    try:
        genre = Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)

    genre.delete()  # safe to delete even if linked to books
    return Response({"message": "Genre deleted successfully"}, status=status.HTTP_200_OK)

