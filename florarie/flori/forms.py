from django import forms
from flori.models import Useri
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactForm(forms.Form):
  contact_name = forms.CharField(required=True)
  contact_email = forms.EmailField(required=True)
  content = forms.CharField(required=True,  widget=forms.Textarea )


class UserForm(forms.ModelForm):
  class Meta:
    model = Useri
    fields = ['email', 'adresa', 'telefon']


class SignUpForm(UserCreationForm):
  adress = forms.CharField(required=True)
  phone_number = forms.CharField(required=True)
  first_name = forms.CharField(max_length=30, required=True)
  last_name = forms.CharField(max_length=30, required=True)
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'adress','phone_number','password1', 'password2',)