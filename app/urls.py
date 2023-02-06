from django.urls import path
from .views import *

urlpatterns = [
	path('', index,name='index'),
	path('add-member', addMember, name='add-member'),
	path('view-member', viewMember, name='view-member'),
	path('edit-member/<int:id>', editMember,name='edit-member'),
	path('delete-member/<int:id>', deleteMember,name='delete-member'),
	path('add-book', addBook, name='add-book'),
	path('view-book', viewBook, name='view-book'),
	path('edit-book/<int:id>', editBook,name='edit-book'),
	path('delete-book/<int:id>', deleteBook,name='delete-book'),
	path('add-book-to-member/<int:id>', addBookToMember,name='add-book-to-member'),
	path('view-books-borrowed/<int:id>', viewBooksBorrowed, name='view-books-borrowed'),
	path('book-return/<int:id>',bookReturn, name='book-return'),
	path('add-book-from-frappe',addBookFormFrappe,name='add-book-from-frappe'),
]