from django.db import models


class User(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    email = models.EmailField(max_length=100, unique=True)
    date_birth = models.DateField(blank=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=10)
    description = models.TextField(max_length=500)






# class MyUser(models.Model):
#     username = models.CharField(max_length=30)
#     password = models.CharField(max_length=30)




