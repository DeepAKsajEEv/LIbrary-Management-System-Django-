from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .forms import MembersForm, BooksForm
import requests
from datetime import datetime
import json


# Create your views here.
def index(request):
    return render (request , 'index.html')

def addMember(request):
    context = {'form' : MembersForm()}
    if request.method == "POST":
        form= MembersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member created Sucessfully')
    return render (request , 'add_member.html', context)

def viewMember(request):
    context = {'members' : Members.objects.all()}
    return render (request , 'view_member.html', context)

def editMember(request,id):
    user = Members.objects.get(id=id)
    EditForm = MembersForm(instance=user)
    if request.method == 'POST':
        EditForm = MembersForm(request.POST, instance=user)
        if EditForm.is_valid():
            EditForm.save()
            messages.success(request, 'Member Edited Sucessfully')
            return redirect('view-member')
    return render(request, 'edit_member.html', {'user': user, 'form': EditForm})

def deleteMember(request, id):
    member = Members.objects.get(id=id)
    member.delete()
    messages.success(request, 'Member was Deletd Sucessfully')
    return redirect("view-member")

def addBook(request):
    context = {'form':BooksForm()}
    if request.method == "POST":
        form= BooksForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created Sucessfully')
            return redirect("view-book")
    return render (request , 'add_book.html' ,context)

def viewBook(request):
    context = { 
        'books':Books.objects.all().filter(is_borrowed=False),
        'books_boowed':Transactions.objects.all().filter(return_status=False),
    }
    return render (request , 'view_book.html', context)
    
def editBook(request,id):
    context = {'form':BooksForm(instance=Books.objects.get(id=id))}
    if request.method == "POST":
        form = BooksForm(request.POST,instance=Books.objects.get(id=id))
        if form.is_valid():
            form.save()
            messages.success(request, 'Book Edited Sucessfully')
            return redirect("view-book")
    return render (request , 'edit_book.html', context)

def deleteBook(request, id):
    book = Books.objects.get(id=id)
    book.delete()
    messages.success(request, 'Book deleted Sucessfully')
    return redirect("view-book")

def addBookToMember(request, id):
    member = Members.objects.get(id=id)
    if member.debt >= 500:
        return redirect("view-member")
        messages.error(request, 'Please return the books already supplied')
    else:
        if request.method == "POST" :
            book_isbn = int(request.POST.get('isbn'))
            book = Books.objects.filter(isbn=book_isbn).first()
            if not book.is_borrowed: 
                try:
                    transact = Transactions(
                            member = member,
                            book = book
                        )
                    transact.save()
                    book.is_borrowed = False
                    book.save()
                    member.debt+=250
                    member.save()
                    messages.success(request, 'Book added to Transaction')
                except:
                    messages.error(request, 'An error occurred, please Try again!')
        return render (request , 'add_Book_To_Member.html')
   




def viewBooksBorrowed(request, id):
    member = Members.objects.get(id = id)

    context = {
    'transactions':member.transactions_set.all().filter(return_status=False),
    'transactions_completed':member.transactions_set.all().filter(return_status=True) 
    }
    return render(request, 'view-books-borrowed.html', context)
    
def bookReturn(request, id):
    transact = Transactions.objects.get(id=id)
    member = transact.member
    book = transact.book
    member.debt = member.debt - 250
    member.save()
    book.is_borrowed=False
    book.save
    transact.return_status= True
    transact.date_returned = datetime.now()
    transact.save()
    messages.success(request, 'Book returned')
    return redirect('view-books-borrowed',id=member.id)

def addBookFormFrappe(request):
    response = requests.get('https://frappe.io/api/method/frappe-library').text
    books= json.loads(response)['message']
    try:
        for i in books:
            try:
                isbn = int(i['isbn'])
            except:
                isbn_str = (i['isbn'])[:-1]
                isbn=int(isbn_str)
            book = Books(
                    title = i['title'],
                    authors=i['authors'],
                    isbn=isbn,
                    publisher=i['publisher'],
                    page=int(i["  num_pages"])
                )
            book.save()
    except:
        messages.error(request, 'Books already imported')
    return redirect('view-book')
