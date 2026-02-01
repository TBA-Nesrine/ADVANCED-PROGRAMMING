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

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_accept_order(request, order_id):
    order = Order.objects.get(id=order_id, status='waiting')
    book = order.book

    if book.quantity < order.quantity:
        return Response({"error": "Not enough stock"}, status=400)

    # 🔥 decrease quantity ONLY NOW
    book.quantity -= order.quantity
    book.save()

    order.status = 'accepted'
    order.save()

    return Response({"message": "Order accepted"})



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

@api_view(['GET'])
def admin_users(request):
    users = User.objects.all()
    return Response(UserSerializer(users, many=True).data)

@api_view(['PATCH'])
def admin_update_user(request, user_id):
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from library_app.models import UserProfile

@api_view(['PATCH'])
def activate_user(request, ref):
    try:
        profile = UserProfile.objects.get(reference_id=ref)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
    profile.active = True
    profile.save()
    return Response({"message": "activated"})

@api_view(['PATCH'])
def deactivate_user(request, ref):
    try:
        profile = UserProfile.objects.get(reference_id=ref)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
    profile.active = False
    profile.save()
    return Response({"message": "deactivated"})


@api_view(['POST'])
def admin_add_user(request):
    """
    API endpoint for admin to add a new user.
    """
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)
