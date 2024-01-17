from django.contrib import admin
from .models import Genre, Book, BookInstance, Author

# Register your models here.
admin.site.register(Genre)
#admin.site.register(Book)
#admin.site.register(BookInstance)
#admin.site.register(Author)


#This code is to create an inline feature of books in the Author detail view
#class BookInline(admin.TabularInline):
      #  model=Book

#Define the new admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display=("first_name", "last_name", "date_of_birth", "date_of_death")

    fields=["first_name", "last_name", ("date_of_birth", "date_of_death")]

    #inlines=[BookInline]



#Register the new admin class with the associated model
admin.site.register(Author, AuthorAdmin)

#Register ModelAdmin classes for both Book and BookInstance using decorators

class BookInstanceInline(admin.TabularInline):
    model= BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=("title", "author")

    inlines=[BookInstanceInline]
    
    
    fieldsets= (
        (None, {
            "fields":("title")
            }),
        ("Book Information", {
            "fields":("summary", "isbn", "genre")
            }),
    )



@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=("book", "status", "borrower", "due_back", "id")
    list_filter=("status", "due_back")
    

    fieldsets= (
        (None, {
            "fields":("book", "imprint", "id")
            }),
        ("Availability", {
            "fields":("status", "due_back", "borrower")
            }),
    )



