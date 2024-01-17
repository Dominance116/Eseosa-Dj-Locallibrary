from django.db import models
from django.urls import reverse
import uuid
from django.conf import settings
from datetime import date

#from django.contrib.auth import get_user_model

# Create your models here.

class Genre(models.Model):
    name=models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. History, Biography, Autography, Romance, etc.)"
)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", args=[str(self.id)])


class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)
    summary=models.TextField(max_length=1000, help_text="Enter brief description of the book")
    isbn= models.CharField("ISBN", max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn' '">ISBN number</a>')
    genre=models.ManyToManyField(Genre, help_text="Select a genre for this book")


    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all () [:3])

    display_genre.short_description="Genre"


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    def Meta(self):
        ordering=["first name"]
    



class BookInstance(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, help_text= "Unique ID for this book across the whole library")
    book= models.ForeignKey('Book', on_delete= models.RESTRICT, null=True)
    imprint=models.CharField(max_length=200)
    due_back=models.DateField(null=True, blank=True)
    borrower=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS=(
        ("m", "Maintenance"),
        ("o", "On Loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status=models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default="m",
        blank=True,
        help_text="Book Availability",
    )

    def __str__(self):
        return f'{self.id} ({self.book.title})' 
    
    
    @property
    def is_overdue (self):
        """Determine is the book is due back based on the current date and the due back date"""
        return bool (self.due_back and date.today () > self.due_back)


    class Meta():
        ordering=["due_back"]
        #permission= (( "can_mark_returned", "Set book as returned"), )



class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(null=True, blank=True)
    date_of_death=models.DateField("died", null=True, blank=True)


    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])
    
    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


    
    class Meta():
        ordering=["first_name", "last_name"]

    




"""

User=get_user_model()

# Create user from model and save to the database
user= User.objects.create_user('myusername', 'myemail@Goddominance.com', 'mypassword')

# Update fields and then save again
user.first_name='Eseosa'
user.last_name='Dominance'
user.save()
"""