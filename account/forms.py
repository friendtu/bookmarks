from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(label='name',max_length=50)
    password=forms.CharField(widget=forms.PasswordInput)

