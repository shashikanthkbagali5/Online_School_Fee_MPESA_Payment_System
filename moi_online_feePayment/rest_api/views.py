# from django.db.models import Q
from students.models import Student
from payment.models import Transaction
from payment.views import stk_push, confirm_payment
from rest_framework import viewsets, permissions, generics, views
from rest_framework.response import Response
from .serializers import StudentSerializer, TransactionSerializer
from twilio.rest import Client
# from django.utils.encoding import smart_unicode
# from rest_framework import renderers


# class PlainTextRenderer(renderers.BaseRenderer):
#     media_type = 'text/plain'
#     format = 'txt'

#     def render(self, data, media_type=None, renderer_context=None):
#         return data.encode(self.charset)

class StudentRudView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Student.objects.all()
	lookup_field = 'pk'
	serializer_class = StudentSerializer

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}


account_sid = 'AC90e0907ae1c4955e99e499ba4f4e100f'
auth_token = '0db92dff3af216d1ec8c3a9f52afcce7'
class WhatsappView(views.APIView):
	def post(self, request):
		client = Client(account_sid, auth_token)
		print(request.POST)
		print(request.POST.get("From"))
		print(request.POST.get("Body"))
		no1 = request.POST.get("From")
		no = no1.split(':')[1]
		bd = request.POST.get("Body")
		# response = ''
		if bd.find('balance') == 0 or bd.find('fee') == 0:
			fee = str(Student.objects.get(phone_no__contains=no[4:]).fee_balance)
			message = client.messages.create(
				from_='whatsapp:+14155238886',
				body='Your fee balance: '+fee,
				to='whatsapp:'+no
				)
			response = message.sid
		else:
			message = client.messages.create(
				from_='whatsapp:+14155238886',
				body='You need to register for an account first',
				to='whatsapp:'+no
				)
			response = message.sid
		print(response)
		return Response(response)

class CallbackView(views.APIView):
	def post(self, request):
		print("we are in the call_back")
		print(self.request.POST)
		response = {
			"ResponseCode":"00000000",
			"ResponseDesc":"success"
		}
		return Response(response)


class StudentListView(generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = StudentSerializer

	def get_queryset(self):
		qs = Student.objects.all()
		query = self.request.GET.get('q')
		if query is not None:
			qs = qs.filter(phone_no__contains=query)
		return qs
	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}
# class StudentViewSet(viewsets.ModelViewSet):
# 	queryset = Student.objects.all()
# 	permission_class = [
# 		permissions.AllowAny

# 	]
# 	serializer_class = StudentSerializer

# Allow to view students fee balance
# class StudentDetailView(generics.RetrieveAPIView):
# 	lookup_field = 'pk'
# 	serializer_class = StudentSerializer

# 	def get_queryset(self):
# 		return Student.objects.all().filter(phone_no=<some_phone_nu>)

# Allow to view allow to view all the transactions
class TransactionListView(generics.ListAPIView):
	pass


# Allow to create transactions -> This is the primary objecive
class TransactionCreateView(generics.CreateAPIView):
	lookup_field = 'pk'
	serializer_class = TransactionSerializer

	def get_queryset(self):
		return Transaction.objects.all()



# USSD API
# confirm_payment(token, shortcode, passwd, timestamp, Crd)
# stk_push(number, amount)

# class USSDView(views.APIView):
# 	# renderer_classes = [PlainTextRenderer]
# 	def post(self, request):
# 		print(request)
# 		print(request.POST)
# 		sess_id = request.POST.get('sessionId')
# 		service_code = request.POST.get('serviceCode')
# 		phone_no = request.POST.get('phoneNumber')
# 		text = request.POST.get('text')
# 		pn = phone_no[len(str(phone_no))-9:]
# 		print(pn)
# 		print(sess_id)
# 		print(service_code)
# 		print(phone_no)
# 		print(text)
# 		if text == "":
# 			response = "CON Please select an action\n"
# 			response += "1. Check Fee Balance\n"
# 			response += "2. Pay Fees"
# 		elif text == "1":
# 			fee = str(Student.objects.get(phone_no__contains=pn).fee_balance)
# 			response = "END Fee Balance: "+fee
# 		elif text == "2":
# 			response = "CON Enter amount to Pay"
# 		else:
# 			# no = phone_no[1:]
# 			print(text.split("*")[1])
# 			# txt = str(text)[2:]
# 			# print(txt)
# 			# response = "END amount = "+ text.split("*")[1]
# 			amount = text.split("*")[1]
# 			amt = int(amount)
# 			state = stk_push(pn, amount)
# 			usr = Student.objects.get(phone_no__contains=pn).username
# 			if state:
# 				print('instance fee balance...')
# 				print(obj.fee_balance)
# 				new_bal = int(obj.fee_balance) - int(amount)
# 				print('printing the new balance...')
# 				print(new_bal)
# 				# This can be potentially catastrophic if two users share the same phone_number
# 				# But who cares :)
# 				Student.objects.filter(username=usr).update(fee_balance=new_bal)
# 				Transaction.objects.create(student=obj, amount=amt, t_type='C', api=False)
# 				msg = "END You have successfully paid "+str(amount)+" via MPESA"
# 				response = msg
# 			else:
# 				response = " END You cancelled the request"
# 		print(response)
# 		return Response(response, content_type='text/plain')
# # Endof the USSD API
