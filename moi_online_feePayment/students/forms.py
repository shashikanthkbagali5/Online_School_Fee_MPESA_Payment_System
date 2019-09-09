from django import forms

from .models import Student

from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class StudentForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"class":"form-control"}))
	class Meta:
		model = Student
		fields = ("name", "reg_no", "group", "programme", "phone_no", "username", "email", "password", "password2", "image")
		widgets={
			"name" : forms.TextInput(attrs={"class":"form-control"}),
			"reg_no" : forms.TextInput(attrs={"class":"form-control"}),
			"group" : forms.Select(attrs={"class":"form-control"}),
			"programme" : forms.Select(attrs={"class":"form-control"}),
			"username" : forms.TextInput(attrs={"class":"form-control"}),
			"phone_no" : forms.TextInput(attrs={"class":"form-control"}),
			"email" : forms.EmailInput(attrs={"class":"form-control"}),
			# "password" : forms.PasswordInput(attrs={"class":"form-control"}),
			# "password2" : forms.PasswordInput(attrs={"class":"form-control"}),
		}

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("Username needs to be Unique")
		return username

	# def clean_reg_no(self):
	# 	reg_no = self.cleaned_data.get('reg_no')
	# 	qs = Student.objects.filter(reg_no=reg_no)
	# 	if qs.exists:
	# 		raise forms.ValidationError("A Student with the same registration Number exists")
	# 	return reg_no

	def clean_phone_no(self):
		no = self.cleaned_data.get('phone_no')
		if no[:1] == '7' or no[:3] == '254' or no[:2] == '07':
			return no
		elif len(no) >= 9 and len(no) <= 12:
			raise forms.ValidationError("The digits should be between 9 and 12")
		else:
			raise forms.ValidationError("Write the Phone Number in the correct format")

	def clean(self):
		data = self.cleaned_data
		password = data.get('password')
		password2 = data.get('password2')
		if password2 != password:
			raise forms.ValidationError("Passwords must match")
		return data

class EditForm(StudentForm):
	def __init__(self, *args, **kwargs):
		super(EditForm, self).__init__(*args, **kwargs)
		self.fields.pop('username')
		self.fields.pop('password')
		self.fields.pop('password2')
	