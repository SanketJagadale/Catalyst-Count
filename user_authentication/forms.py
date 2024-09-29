
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from authenticationdemoapp.models import CustomUser


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    # country = forms.ChoiceField(choices=CustomUser.COUNTRY_CHOICES, required=True)
    # address = forms.CharField(max_length=30, required=True)

    class Meta:
        #model = CustomUser
        model=User
        #fields = ['username','first_name','last_name','email','country','address']
        fields = ['username','first_name','last_name','email']