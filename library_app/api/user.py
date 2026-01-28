from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from ..models import Book, Order, Review
from ..serializers import BookSerializer, OrderSerializer

@api_view(['GET'])
def user_books(request):
    books = Book.objects.all()
    return Response(BookSerializer(books, many=True).data)

@api_view(['POST'])
def user_borrow_book(request):
    book = Book.objects.get(id=request.data['book_id'])
    if book.quantity <= 0:
        return Response({"error": "not available"}, status=400)

    Order.objects.create(user=request.user, book=book, quantity=1)
    book.quantity -= 1
    book.save()

    return Response({"message": "book borrowed"})

@api_view(['GET'])
def user_mybag(request):
    orders = Order.objects.filter(user=request.user, date_return__isnull=True)
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['POST'])
def user_return_book(request):
    order = Order.objects.get(id=request.data['order_id'])
    order.date_return = timezone.now()
    order.save()

    book = order.book
    book.quantity += order.quantity
    book.save()

    return Response({"message": "returned"})

@api_view(['POST'])
def user_feedback(request):
    Review.objects.create(
        user=request.user,
        book_id=request.data.get('book_id'),
        feedback=request.data['feedback']
    )
    return Response({"message": "feedback sent"})
