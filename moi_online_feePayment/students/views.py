from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from .models import Student
from .forms import StudentForm, LoginForm, EditForm
from django.views.decorators.csrf import csrf_exempt
from payment.views import stk_push

from django.db.models import Q
from django.conf import settings

from payment.models import Transaction
from django.contrib import messages
from datetime import datetime
import string, random
import africastalking

# comment this out when not talking to the at api on server
africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
# Change so that the username corresponds to the registration number


def student_detail(request, *args, **kwargs):
	print("Printing the user....	")
	print(request.user)
	if request.user.is_staff:
		# return redirect('/admin')
		return redirect('bill_')

	elif request.user.is_authenticated:
		obj = Student.objects.get(username=request.user)
		context = {
			'object':obj,
		}
		return render(request, "student/detail.html", context)
	else:
		return redirect('log__in')

def edit_student(request, *args, **kwargs):
	print(request)
	# print(dir(request))
	# print(request.path.replace('/', ''))
	stud = get_object_or_404(Student, username=request.user)
	# initial_data = {
	# 	'name':stud.name,
	# 	'reg_no':stud.reg_no,
	# 	'group': stud.group_id,
	# 	'programme':stud.programme,
	# 	'phone_no':stud.phone_no,
	# 	'email': stud.email,
	# 	'image': stud.image,
	# }
	if request.method == 'GET':
		print('the method is get')
		# form = EditForm(initial=initial_data)
		form = EditForm(instance=stud)
	elif request.method == 'POST':
		form = EditForm(request.POST or None, request.FILES, instance=stud)
		print('the method is post')
		if form.is_valid():
			print(form.data['name'])
			print(form.cleaned_data)
			form.save(commit=False)
			stud.save()
			print('the form has been saved')
			# Redirect Student to homepage after a successful save so 
			# that they can see how their changes have taken effect
			return redirect('student_home')
		else:
			print(form.errors)
	context = {
		'form':form,
	}
	return render(request, "student/create.html", context)


def log_in(request):

	form = LoginForm(request.POST or None)
	
	context = {
	'form':form,

	}
	if request.method == 'GET':
		context['cred'] = True
		print("method is get")
	if form.is_valid():
		print(form.cleaned_data)
		context['data'] = form.cleaned_data
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You have successfully logged in")
			return redirect("student_home")
		else:
			print('we are here')
			context['form'] = LoginForm()
			messages.error(request, "Enter the correct credentials to login else register for an account")
	return render(request, "student/login.html",context)


User = get_user_model()
def student_create(request, *args, **kwargs):
	if request.user.is_staff:
		return HttpResponseForbidden('<h1>You are not a student <b>:(</b></h1>')
	form = StudentForm(request.POST or None)
	context = {
		'form':form,
	}
	if form.is_valid():
		print(form.cleaned_data)
		print(dir(form.cleaned_data))
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		email = form.cleaned_data.get('email')
		new_user = User.objects.create_user(username, email, password)
		# the commented methods below did not seem to work as I had expected
		# form.cleaned_data.pop('password')
		# form.cleaned_data.pop('password2')
		print(form.cleaned_data)
		form.save()
		return redirect("student_home")
	return render(request, "student/create.html", context)


def log_out(request):
	logout(request)
	return redirect('student_home')

def search(request, *args, **kwargs):
	if not request.user.is_staff:
		raise PermissionDenied()
		
	query = request.GET.get('q', None)
	print(request)
	# remember to add a disticnct filter method so that it does no return the same object twice
	lookup = Q(reg_no__icontains=query) | Q(name__icontains=query)
	obj = Student.objects.filter(lookup)
	if obj.count() > 0:
		if obj.count() == 1:
			msg = "Found one student matching your criteria"
		else:
			msg = "Found " + str(obj.count()) + " students matching your criteria"
		messages.success(request, msg, extra_tags='messagelist')
	else:
		messages.error(request, 'No students match your criteria', extra_tags='errormsg padd')
	print(obj)
	searched = True
	credits = Transaction.objects.filter(t_type='C')
	debits = Transaction.objects.filter(t_type='D')
	context = {
		'list':obj,
		's': searched,
		'credits':credits,
		'debits':debits,
	}
	return render(request, 'student/students.html', context)

def students_list(request):
	if not request.user.is_staff:
		# return HttpResponseForbidden('<h1>Forbidden</h1>')
		raise PermissionDenied()
	student_list = Student.objects.all()
	credits = Transaction.objects.filter(t_type='C')
	debits = Transaction.objects.filter(t_type='D')
	context = {
		'list':student_list,
		'credits':credits,
		'debits':debits,
	}
	return render(request, 'student/students.html', context)


def exam_card(request):
	sms = africastalking.SMS
	student = Student.objects.get(username=request.user)
	courses = student.programme.units.all()
	# Generate timestamp
	timestamp = str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '').replace('.', '')
	#ftm for formatted time
	ftm = datetime.now().strftime("%A %dth %B %Y")
	# Generate a random string
	chars = string.ascii_uppercase + string.digits
	rst = ''.join(random.choice(chars) for _ in range(15))
	msg = "Timestamp: "+timestamp+"\n"+"Serial No: "+rst
	# msg = 'hello there'
	# sms code

	def on_finish(error, response):
	    if error is not None:
	        raise error
	    print(response)
	sms.send(msg, ["+254711836533"], "MusoEdu") 
	# send text message to the student here
	context = {
		"student": student,
		"courses": courses,
		'ftm':ftm,
		'timestamp':timestamp,
		'rst': rst,
	}
	return render(request, 'student/exam_card.html', context)


@csrf_exempt
def ssd_test(request):
	print(request)
	print(request.POST)
	sess_id = request.POST.get('sessionId')
	service_code = request.POST.get('serviceCode')
	phone_no = request.POST.get('phoneNumber')
	text = request.POST.get('text')
	pn1 = phone_no[len(str(phone_no))-9:]
	pn = '254'+pn1
	print(sess_id)
	print(service_code)
	print(phone_no)
	print(text)
	if text == "":
		response = "CON Please select an action\n"
		response += "1. Check Fee Balance\n"
		response += "2. Pay Fees"
	elif text == "1":
		phone_no = phone_no[len(str(phone_no))-9:]
		fee = str(Student.objects.get(phone_no__contains=phone_no).fee_balance)
		response = "END Fee Balance: "+fee
	elif text == "2":
		response = "CON Enter amount to Pay"
	else:
		# no = phone_no[1:]
		print(text.split("*")[1])
		txt = str(text)[2:]
		print(txt)
		response = "END amount = "+ text.split("*")[1]
		amount = text.split("*")[1]
		amt = int(amount)
		state = stk_push(pn, amount)
		# usr = Student.objects.get(phone_no__contains=pn).username
		if state:
			obj = Student.objects.get(phone_no__contains=pn1)
			print('instance fee balance...')
			print(obj.fee_balance)
			new_bal = int(obj.fee_balance) - int(amount)
			print('printing the new balance...')
			print(new_bal)
			# This can be potentially catastrophic if two users share the same phone_number
			# But who cares :)
			# or you can simply make sure that only one person is returned before the update
			# Maybe add it as a validation in the form itself
			Student.objects.filter(phone_no__contains=pn1).update(fee_balance=new_bal)
			Transaction.objects.create(student=obj, amount=amt, t_type='C', api=False)
			# msg = "END You have successfully paid "+amount+" via MPESA"			
			response = "END You have successfully paid "+amount+" via MPESA"
		else:
			response = "END You cancelled the request"
	print('printing the message...')
	print(response)
	# print(HttpResponse(response))
	return HttpResponse(response)