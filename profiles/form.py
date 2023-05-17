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


class SignUpForm(forms.Form):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'date_birth', 'password', 'phone_number')

    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "signUpName", 'type': "text", 'name': "sign_up_name", 'required': ""}))
    surname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "signUpSurname", 'type': "text", 'name': "sign_up_surname", 'required': ""}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "signUpEmail", 'type': "email", 'name': "sign_up_email", 'required': ""}))
    date_birth = forms.DateField(widget=forms.DateInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "signUpDateBirth", 'type': "date", 'name': "sign_up_date_birth", 'required': ""
    }))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "signUpPassword", 'type': "password", 'name': "sign_up_password", 'required': ""}))
    phone_number = forms.EmailField(max_length=20, widget=forms.TextInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "signUpPhoneNumber", 'type': "text", 'name': "sign_up_phone_number", 'required': ""}))

