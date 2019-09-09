# from django.db import models
from django import forms
# from django.forms import ModelForm
from students.models import Group
from .models import Transaction

class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = '__all__'
		localized_fields = '__all__'
		widgets = {
			"group":forms.TextInput(attrs={"class":"form-control"}),
			"amount":forms.TextInput(attrs={"class":"form-control"}),
		}