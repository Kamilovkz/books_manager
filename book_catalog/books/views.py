from rest_framework.response import Response
from .serializers import (
    UserSerializer, BookSerializer, BookOneSerializer, FavoriteSerializer)
from users.models import CustomUser
from .models import Book, FavoriteBook
from rest_framework import generics, permissions, status

class UserBooksView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BooksView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        book_id = self.request.query_params.get('book_id')
        if book_id is not None:
            return BookOneSerializer
        return BookSerializer

    def get_queryset(self):
        book_id = self.request.query_params.get('book_id')
        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')
        genre = self.request.query_params.get('genre')

        queryset = Book.objects.all()

        if book_id is not None:
            # FILTER BY BOOK_ID
            queryset = Book.objects.filter(id=book_id)

        if from_date is not None and to_date is not None:
            # FILTER BY DATE RANGE
            queryset = queryset.filter(publication_date__range=(from_date, to_date))

        if genre is not None:
            # FILTER BY GENRE
            queryset = Book.objects.filter(genre=genre)

        return queryset
    
class FavoriteBookView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        book = request.data.get('book')

        if book_id and book:
            return Response({'message': 'Provide either "book_id" or "book", not both.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not book_id and not book:
            return Response({'message': 'One of "book_id" or "book" is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if book_id:
            try:
                favorite_book = FavoriteBook.objects.get(user=self.request.user, book__id=book_id)
                favorite_book.delete()
                return Response({'message': 'Book added to favorites'}, status=status.HTTP_204_NO_CONTENT)
            except FavoriteBook.DoesNotExist:
                pass

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        # Get the book_id from the URL parameters
        book_id = request.data.get('book')

        try:
            favorite_book = FavoriteBook.objects.get(user=self.request.user, book=book_id)
            favorite_book.delete()
            return Response({'message': 'Book removed from favorites'}, status=status.HTTP_204_NO_CONTENT)
        except FavoriteBook.DoesNotExist:
            return Response({'message': 'Book not found in favorites'}, status=status.HTTP_404_NOT_FOUND)
