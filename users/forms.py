from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.models import Profile


class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
	username = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control border-start-0',
		"type":"text",
		"placeholder":"Email Address"

	}))

	password = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control border-start-0',
		"type":"password",
		"placeholder":"Password"

	}))
	# mob = forms.IntegerField() # newly added

	# class Meta:
	# 	model = User
	# 	fields = ('username','email','password1')
		# widgets = {
		# 	'first_name':forms.TextInput(attrs={'class':'','placeholder':'First Name'}),
		# 	'last_name':forms.TextInput(attrs={'class':'','placeholder':'Last Name'}),
		# 	'username':forms.TextInput(attrs={'class':'','placeholder':'username'}),
		# 	'email':forms.TextInput(attrs={'class':'','placeholder':'Email'}),
			
		# }
# class UserInfoForm(forms.ModelForm):
# 	mobile = forms.IntegerField(widget=forms.TextInput(attrs={
# 		'class': 'form-control ps-15 bg-transparent',
# 		'placeholder': 'Phone Number',

# 	}))
# 	class Meta():
# 		model = Profile
# 		fields = ['mobile']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']