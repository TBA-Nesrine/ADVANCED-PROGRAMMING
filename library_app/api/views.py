from django.shortcuts import render

def home(request):
    return render(request, 'library_app/templates/user_home.html')  # or user_home.html


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from library_app.models import Book, Review

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review_api(request, book_id):
    """
    API endpoint to add a review to a book
    """
    user = request.user
    book = Book.objects.filter(id=book_id).first()
    if not book:
        return Response({"error": "Book not found"}, status=404)

    rating = request.data.get("rating")
    comment = request.data.get("comment", "")

    if not rating:
        return Response({"error": "Rating is required"}, status=400)

    # Save the review
    review = Review.objects.create(
        book=book,
        user=user,
        rating=rating,
        comment=comment
    )

    return Response({
        "message": "Review added successfully",
        "review": {
            "id": review.id,
            "book": book.title,
            "rating": review.rating,
            "comment": review.comment,
            "user": user.username
        }
    })
