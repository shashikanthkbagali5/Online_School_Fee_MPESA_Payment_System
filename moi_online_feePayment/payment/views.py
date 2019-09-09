from django.shortcuts import render, redirect
import json

from requests.auth import HTTPBasicAuth
# from .views import stk_push

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
import requests
from students.models import Student
from .models import Transaction
from students.models import Group
from datetime import datetime, timedelta
from django.contrib import messages
from base64 import b64encode

import time

# dt = datetime.now()
# from .forms import GroupForm
# The admin has the potential to manipulate the fee balance via addition
# while the the payment process should negate it
# Produce a report of the transaction history
# No need for ajax in the billing html as we are only reacting to the state 
# of the checkbox

# Any new transction should be an instance of the transaction class
# thus the transaction history will simply refer to all objects of the class
def fee_report(request):
	fee_bal = str(Student.objects.get(username=request.user).fee_balance)
	# Should return the fee balance of the logged in student and
	# displays a form composed of an input field and a button to
	# enter and submit the amount of fees they want to pay.
	# After the processing is done, they fee balance should be able
	# reflect...
	context = {
		'balance':fee_bal,
	}
	return render(request, 'payment/payment.html', context)

def statements(request):
	# deb_ = {}
	# cred_ = {}
	stud = Student.objects.get(username=request.user)
	entry = Transaction.objects.filter(student=stud)
	# if entry is not None:
	# 	cr = entry.filter(t_type='C')
	# 	dbt	= entry.filter(t_type='D')
	# 	for c in cr:
	# 		deb_[c.id] = c.amount
	# 	for d in dbt:
	# 		cred_[d.id] = d.amount
	# dumps method converts a dictionary to a string object
	# credits = json.dumps(deb_, default=lambda x:str(x))
	# credits = '{"legend":2, "actor":2}'
	# debits = json.dumps(cred_, default=lambda x:str(x))

	credits = entry.filter(t_type='C')
	debits = entry.filter(t_type='D')
	# loads probable retrieves the converted method
	# credit = json.loads(js1)
	# debits = json.loads(js2)
	c_count = entry.filter(t_type='C').count()
	d_count = entry.filter(t_type='D').count()
	e_count = entry.count()
	name = stud.name
	print(credits)
	print(str(debits))
	context = {
		'entries':entry,
		'student':stud,
		'credits' : credits,
		'debits':debits,
		'c_count': c_count,
		'd_count': d_count,
		'e_count': e_count,
		'name':name
	}
	return render(request, 'payment/statement.html', context)

# The function below will be replaced with the stk push

# Since the staff member does not possess the capacity to alter the group,
# simply display the data in a table directly from the database, then using
# the data from the database determine the students' group in order to decide
# how much to bill them

def bill(request):
	if not request.user.is_staff:
		raise PermissionDenied()
	grp = Group.objects.all()
	print(request.POST)
	print('attempting to print the boolean values...')
	# this loop is meant to set the new values of the student session
	# the POST method returns 'on' or None

	for gr in grp:
		print(request.POST.get(gr.group))
		# Check if the key corresponds to the current entry's group

		if request.POST.get(gr.group) == 'on':
			gr.in_session=True
			gr.save()
		elif request.POST.get(gr.group) is None:
			gr.in_session=False
			gr.save()

# Add a test that checks for deferrement
	m_check = False
	if request.POST:
		for obj in Group.objects.all():
			# Add a check to ensure that all billed students are in session
			# print('printing whether in session...')
			# print(obj.in_session)
			if obj.in_session:
				for stud in Student.objects.all():
					# you need to check if the groups correspond
					# print('is the obj year_sem < the programme duration')
					# print(not int(obj.year_sem) >= stud.programme.duration)
					# Added the duration times 2 to account for the 2 semesters in an academic year
					if obj.group == stud.group.group and not stud.deferred and not int(obj.year_sem) >= stud.programme.duration*2:
						in_amount=int(stud.group.amount)
						fee = int(stud.fee_balance)
						new_b = in_amount + fee
						print("printing the group amount...")
						print(in_amount)
						print("printing the fee balance...")
						print(fee)
						print("printing the new balance...")
						print(new_b)
						# The commented method below also seems to work perfectly
						# Student.objects.filter(group=obj).update(fee_balance=new_b)
						# The two statements below have replaced the statement above
						stud.fee_balance=new_b
						stud.save()
						Transaction.objects.create(student=stud, amount=in_amount, t_type='D', api=False)
						m_check=True
						ys = int(obj.year_sem)
						ys += 1
						obj.year_sem=str(ys)
						obj.save()

	# form = GroupForm(request.POST or None)

	# print(request.POST.get('sess'))
	# amt = request.POST.get('amount')
	# you need a way to select groups currently in session
	if m_check:
		messages.success(request, "All students in session have been billed successfully")
	context = {
		# "form":form,
		'group':grp,
	}
	return render(request, 'payment/bill.html', context)

def test(request):
	str_except=False
	print(request)
	print('printing the amount to pay....')
	print(request.GET.get('bal'))
	obj = Student.objects.get(username=request.user)
	print(obj.phone_no)
	no = obj.phone_no
	if no[:2] == '07':
		no1 = '254' + no[1:]
	elif no[:3] == '254':
		no1 = no
	elif no[:1] == '7':
		no1 = '254' + no

	# print(no1)
	# print(len(no1))
	# check if the amount is a number otherwise pass an error message and reload the page
	amount = request.GET.get('bal' or None)
	if amount is not '':
		try:
			amount = int(amount)
			if amount == 0:
				return redirect('fees_')
		except:
			str_except=True
			messages.error(request, "Please enter the amount as a number inorder to pay", extra_tags='errormsg padd')
			print(dir(messages))
			return redirect('fees_')
		# except ValueError:
		# 	str_except=True
		# 	messages.error(request, "Please enter the amount as a number inorder to pay")
	else:
		return redirect('fees_')
	# call the get token method
	# nw = dt + timedelta(minutes = 55)
	# if nw >= datetime.now():
		# token = get_token()
		# print(token)
	# token = get_token()
	state = stk_push(no1, amount)
	# place the stk push function here and whatever retuns, cut out the details and
	# add them into the database
	if state:
		print('instance fee balance...')
		print(obj.fee_balance)
		new_bal = int(obj.fee_balance) - amount
		print('printing the new balance...')
		print(new_bal)
		Student.objects.filter(username=request.user).update(fee_balance=new_bal)
		Transaction.objects.create(student=obj, amount=amount, t_type='C', api=False)
		msg = "You have successfully paid "+str(amount)+" via MPESA"
		print(msg)
		messages.success(request, msg, extra_tags='messagelist')
	else:
		messages.success(request, "Please confirm the transaction to proceed", extra_tags='messagelist')
	return redirect('fees_')


def get_token():
	dt = datetime.now()
	consumer_key = "3aLkEp8qLP7lmFcxXrAHu4Deh7PdkLOo"
	consumer_secret = "GDyQhCSm49GwZ9Re"
	api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
	r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
	print (r.text)
	print(r.content)
	pd = json.loads(r.text)
	print("printing the pd....")
	# print(pd)
	token = pd['access_token']
	# print(dir(r))
	# return HttpResponse(token)
	return token

def stk_push(number, amount):
	# code to generate a timestamp
	token = get_token()
	# token = "ZDxzYjNFVdPyhMSWSjgzQ0SXQ1DD"
	timestamp = str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '')[:14]
	shortcode = "174379"
	passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
	stt = shortcode + passkey+timestamp
	# Generate the base64 password automatically
	passwd = str(b64encode(stt.encode())).replace("'", "")[1:]
	access_token = token
	api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
	headers = { "Authorization": "Bearer %s" % access_token }
	request = { 
		"BusinessShortCode": shortcode,
		"Password": passwd,
		"Timestamp": timestamp,
		"TransactionType": "CustomerPayBillOnline",
		"Amount": amount,
		"PartyA": number,
		"PartyB": shortcode,
		"PhoneNumber": number,
		"CallBackURL": "https://a3d94412.ngrok.io/api/call/",
		"AccountReference": "Roy Kathurima",
		"TransactionDesc": "test" }
	response = requests.post(api_url, json = request, headers=headers)
	print('stkpush process request results......')
	print (response.text)
	rt = json.loads(response.text)
	rsp = rt['ResponseCode']
	Crd = rt['CheckoutRequestID']
	state = False
	if rsp == '0':
		time.sleep(15)
		state=confirm_payment(token, shortcode, passwd, timestamp, Crd)
	print('printing the state')
	print(state)
	return state
# API




# def call_back(request):
# 	print("we are in the call_back")
# 	print(request)
# 	response = {
# 		"ResponseCode":"00000000",
# 		"ResponseDesc":"success"
# 	}
# 	return JsonResponse(response)



# Maybe send a text to the user to shw them that their transaction was successful
def confirm_payment(token, shortcode, passwd, timestamp, Crd):
	access_token = token
	api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
	headers = {"Authorization": "Bearer %s" % access_token}
	request = { "BusinessShortCode": shortcode,
	      "Password": passwd,
	      "Timestamp": timestamp,
	      "CheckoutRequestID": Crd,
	}

	response = requests.post(api_url, json = request, headers=headers)
	print('stk query results......')
	print (response.text)
	resp = json.loads(response.text)
	rsc = resp['ResultCode']
	if rsc:
		print('printing the ResultCode...')
		print(rsc)
		if rsc == '0':
			return True
	return False