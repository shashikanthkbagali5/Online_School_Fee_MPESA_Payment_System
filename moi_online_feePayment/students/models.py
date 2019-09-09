import random, os
from django.db import models
from rest_framework.reverse import reverse as api_reverse

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1,9999999999)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"media/{new_filename}/{final_filename}"

class Course(models.Model):
	code 	= models.CharField(max_length=10)
	title	= models.CharField(max_length=100)
	units	= models.IntegerField(default=3)

	def __str__(self, *args, **kwargs):
		return self.title

class Programme(models.Model):
	programme 	= models.CharField(max_length=200)
	duration	= models.IntegerField(default=4)
	units		= models.ManyToManyField(Course, blank=True)
	# the field below would store values such as 'TED'
	# would be used to clearly identify the programmes programmatically
	# or maybe can be a charfield but with choices
	# they key can be converted to an int and back in event of a computation
	# disp 		= models.CharField(max_length=10)

	def __str__(self, *args, **kwargs):
		return self.programme

class Group(models.Model):
	mwaka 		= (
	('1', 'Year I Semester I'),
	('2', 'Year I Semester II'),
	('3', 'Year II Semester I'),
	('4', 'Year II Semester II'),
	('5', 'Year III Semester I'),
	('6', 'Year III Semester II'),
	('7', 'Year IV Semester I'),
	('8', 'Year IV Semester II'),
	('9', 'Year V Semester I'),
	('10','Year V Semester II'),
	('11','Year VI Semester I'),
	('12','Year VI Semester II'),
	)
	group 		= models.CharField(max_length=15)
	amount		= models.DecimalField(max_digits=10, decimal_places=0, default=5)
	in_session 	= models.BooleanField(default=False)
	# Should be a positive integer in the range 1..12
	year_sem	= models.CharField(default='8', choices=mwaka, max_length=1)

	def __str__(self, *args, **kwargs):
		return self.group

class Student(models.Model):
	name		= models.CharField(max_length=100)
	email		= models.EmailField(null=True, blank=True)
	# password	= models.CharField(null=True, blank=True, max_length=20)
	# password2	= models.CharField(null=True, blank=True, max_length=20)
	username	= models.CharField(null=True, blank=True, max_length=20)
	reg_no		= models.CharField(max_length=20)
	# group		= models.CharField(max_length=20)
	group 		= models.ForeignKey(Group, on_delete=models.CASCADE)
	programme	= models.ForeignKey(Programme, on_delete=models.CASCADE)
	phone_no	= models.CharField(max_length=15)
	image		= models.ImageField(null=True, blank=True, upload_to=upload_image_path)
	fee_balance	= models.DecimalField(max_digits=10, decimal_places=0, default=0)
	deferred 	= models.BooleanField(default=False)
	

	def __str__(self, *args, **kwargs):
		return self.name

	def get_api_url(self, request=None):
		return api_reverse("api_:s_detail", kwargs={'pk':self.pk}, request=request)
		# return api_reverse("api_:s_list", request=request)


