
from rest_framework.response import Response
from django.utils import timezone
from ..models import Book, Order, Review
from ..serializers import BookSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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


# api/users.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from library_app.models import Book, Review
from django.db.models import Avg

def add_review_for_user(user, book_id, rating, comment=""):
    """
    Adds a review for a book by a user.
    Returns a dict with 'success' and 'review' or 'error'.
    """
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return {"success": False, "error": "Book not found"}

    try:
        rating = int(rating)
    except (ValueError, TypeError):
        return {"success": False, "error": "Rating must be a number"}

    review = Review.objects.create(
        book=book,
        user=user,
        rating=rating,
        comment=comment
    )

     # Update book's average rating
    avg_rating = Review.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
    book.reviews = round(avg_rating, 1)  # keep 1 decimal place
    book.save()

    return {
        "success": True,
        "review": {
            "id": review.id,
            "book": book.title,
            "rating": review.rating,
            "comment": review.comment,
            "user": user.username
        }
    }

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library_app.models import Book, Review


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_book_details(request, book_id):

    book = Book.objects.get(id=book_id)

    reviews = Review.objects.filter(book=book).select_related('user')

    reviews_data = [
        {
            "username": review.user.username,
            "comment": review.comment
        }
        for review in reviews
    ]

    return Response({
        "book": {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "quantity": book.quantity,
            "image": book.image.url if book.image else None,
        },
        "reviews": reviews_data
    })


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library_app.models import Contact, Book

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_send_contact(request):

    message = request.data.get('feedback')
    book_id = request.data.get('book_id')

    if not message:
        return Response(
            {"error": "Message cannot be empty"},
            status=400
        )

    book = None
    if book_id:
        book = Book.objects.filter(id=book_id).first()

    Contact.objects.create(
        user=request.user,
        book=book,
        message=message
    )

    return Response({"message": "Message sent successfully"})
