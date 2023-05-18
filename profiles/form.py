from django import forms
from django.contrib.auth.hashers import make_password

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
        fields = ('name', 'surname', 'email', 'date_birth', 'password', 'phone_number', 'description', 'role')

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
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "signUpPhoneNumber", 'type': "text", 'name': "sign_up_phone_number", 'required': ""}))
    description = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': "form-control shadow-0 px-0 border-0 border-bottom",
        'id': "signUpDescription", 'type': "text", 'name': "sign_up_description", 'required': ""}))

    role = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'my-checkbox-class',
        'id': "signUpRole", 'type': "text", 'name': "sign_up_role", 'required': ""
    }))

    def save(self):
        user = User()
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']
        user.date_birth = self.cleaned_data['date_birth']
        user.password = make_password(self.cleaned_data['password'])
        user.phone_number = self.cleaned_data['phone_number']
        user.description = self.cleaned_data['description']
        if self.cleaned_data['role']:
            user.role = 'teacher'
        else:
            user.role = 'user'
        user.save()
        return user



