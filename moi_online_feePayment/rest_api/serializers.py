from rest_framework import serializers
from students.models import Student
from payment.models import Transaction

# Student serializer

class StudentSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField(read_only = True)
	class Meta:
		model = Student
		fields = '__all__'
		# fields = [
		# 	'pk',
		# 	'url',
		# 	'name',
		# 	'reg_no'
		# ]
	def get_url(self, obj):
		request = self.context.get('request')
		return obj.get_api_url(request=request)

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = '__all__'
		# fields = [
		# 	'amount',
		# 	't_type',
		# 	'student',
		# 	]
		read_only_fields = ['id', 'timestamp']