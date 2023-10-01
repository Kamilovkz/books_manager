from django.db import models
from users.models import CustomUser

# Book models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    text = models.TextField()
    
    def save(self, *args, **kwargs):
        reviews = Review.objects.filter(book=self.book)
        total_rating = sum([review.rating for review in reviews])
        
        if len(reviews) > 0:
            self.book.average_rating = total_rating / len(reviews)
            self.book.average_rating = round(self.book.average_rating, 2)
        else:
            self.book.average_rating = self.rating
        
        self.book.save()
        super(Review, self).save(*args, **kwargs)
 
        
    def __str__(self) -> str:
        return f"{self.book.title} review from {self.user.username}"

class FavoriteBook(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.book.title}"

