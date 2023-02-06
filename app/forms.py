from django import forms
from .models import *

class MembersForm(forms.ModelForm):
    class Meta:
        model = Members
        exclude = ['debt']



class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        exclude = ['is_borrowed']
        