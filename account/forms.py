from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username=forms.CharField(label='name',max_length=50)
    password=forms.CharField(widget=forms.PasswordInput)

class UserRegistrationFrom(ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label="Repeat Passowrd",widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','email']
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

class UserEditForm(ModelForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email')

class ProfileEditForm(ModelForm):
    class Meta:
        model=Profile
        fields=('date_of_birth','photo')




