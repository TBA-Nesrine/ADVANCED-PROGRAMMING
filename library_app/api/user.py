
from rest_framework.response import Response
from django.utils import timezone
from ..models import Book, Order, Review
from ..serializers import BookSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from library_app.models import UserProfile
from django.contrib.auth.models import User
from library_app.serializers import UserSerializer

@api_view(['GET'])
def user_books(request):
    books = Book.objects.all()
    return Response(BookSerializer(books, many=True).data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_borrow_book(request):
    book = Book.objects.get(id=request.data['book_id'])

    if book.quantity <= 0:
        return Response({"error": "Book not available"}, status=400)

    Order.objects.create(
        user=request.user,
        book=book,
        quantity=1,
        status='waiting'
    )

    return Response({"message": "Order sent, waiting for admin approval"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_mybag(request):
    orders = Order.objects.filter(
        user=request.user,
        status='waiting'
    )
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_cancel_order(request):
    order = Order.objects.get(
        id=request.data['order_id'],
        user=request.user,
        status='waiting'
    )
    order.delete()
    return Response({"message": "Order cancelled"})


@api_view(['POST'])
def user_return_book(request):
    order = Order.objects.get(id=request.data['order_id'])
    order.date_return = timezone.now()
    order.save()

    book = order.book
    book.quantity += order.quantity
    book.save()

    return Response({"message": "returned"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_read_books(request):
    orders = Order.objects.filter(
        user=request.user,
        status='accepted'
    )
    return Response(OrderSerializer(orders, many=True).data)


@api_view(['POST'])
def user_feedback(request):
    Review.objects.create(
        user=request.user,
        book_id=request.data.get('book_id'),
        feedback=request.data['feedback']
    )
    return Response({"message": "feedback sent"})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from library_app.models import UserProfile
from library_app.serializers import UserProfileSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from library_app.serializers import UserSerializer


@api_view(['GET'])
def get_user_profile(request):

    serializer = UserSerializer(request.user)
    return Response(serializer.data)



@api_view(['PUT'])
def update_user_profile(request):

    serializer = UserSerializer(
        request.user,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework import status

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    form = PasswordChangeForm(request.user, request.data)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # keep user logged in
        return Response({"message": "Password changed successfully"})
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
