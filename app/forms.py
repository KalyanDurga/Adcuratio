from django import forms
from app.models import *

class Userform(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={'password':forms.PasswordInput}

class TravelForm(forms.ModelForm):
    class Meta:
        model=Travel
        fields='__all__'