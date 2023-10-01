from rest_framework import serializers
from .models import Review, FavoriteBook, Book
from users.models import CustomUser

class ReviewSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['rating', 'text', 'book_title', 'username']


class UserSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    def get_books(self, instance):
        user = self.context['request'].user
        favorite_books = FavoriteBook.objects.filter(user=user)
        serialized_books = []

        for favorite_book in favorite_books:
            book = favorite_book.book
            serialized_book = {
                'id': book.id,
                'title': book.title,
                'favorite': True,
                'reviews': ReviewSerializer(book.review_set.all(), many=True).data
            }
            serialized_books.append(serialized_book)

        return serialized_books

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'books']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    def get_author(self, instance):
        return instance.author.name

    def get_is_favorite(self, instance):
        return FavoriteBook.objects.filter(
            user=self.context['request'].user, book=instance).exists()

    class Meta:
        model = Book
        fields = [
            'id', 
            'title', 
            'publication_date', 
            'description', 
            'average_rating', 
            'genre', 
            'author',
            'is_favorite']

class BookOneSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def get_genre(self, instance):
        return instance.genre.name
    
    def get_author(self, instance):
        return instance.author.name
    
    def get_reviews(self, instance):
        reviews = Review.objects.filter(book=instance).order_by('-id')
        return ReviewSerializer(reviews, many=True).data
    

    class Meta:
        model = Book
        fields = [
            'id', 
            'genre', 
            'author', 
            'title', 
            'publication_date', 
            'description', 
            'average_rating', 
            'reviews'
            ]

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = ['book']
        read_only_fields = ['user']
    def validate(self, data):
        # Get the user from the request context
        user = self.context['request'].user

        # Check if a favorite entry for the same book already exists for the user
        existing_favorite = FavoriteBook.objects.filter(user=user, book=data['book']).first()

        if existing_favorite:
            raise serializers.ValidationError('This book is already in your favorites.')

        return data