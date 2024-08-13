from django import forms
from .models import Form1

class Form1Form(forms.ModelForm):
    class Meta:
        model = Form1
        fields = '__all__'  # You can specify the fields explicitly if needed
