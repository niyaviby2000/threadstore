from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","password1","password2"]

class SignInForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField()



    

