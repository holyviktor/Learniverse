from django import forms

from profiles.models import User


class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ('email', 'password')

    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "resEmail", 'type': "email", 'name': "res_email", 'required': ""}))

    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "resPassword", 'type': "password", 'name': "res_password", 'required': ""}))



