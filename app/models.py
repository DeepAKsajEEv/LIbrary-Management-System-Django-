from django.db import models
from datetime import datetime,timedelta


# Create your models here.
class Members(models.Model):
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	debt = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.firstname

class Books(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    isbn = models.IntegerField(unique=True)
    publisher = models.CharField(max_length=200)
    page = models.IntegerField()
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

def get_returndate():
    return datetime.today() + timedelta(days=7)

def get_now():
	return datetime.now()

class Transactions(models.Model):
	member = models.ForeignKey('Members', on_delete=models.CASCADE)
	book = models.ForeignKey('Books', on_delete=models.CASCADE)
	issue_date = models.DateTimeField(default=get_now())
	due_date = models.DateTimeField(default=get_returndate())
	date_returned=models.DateField(null=True, blank=True)
	return_status = models.BooleanField(default=False)
