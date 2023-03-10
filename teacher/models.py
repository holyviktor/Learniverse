from django.db import models


# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_lenght=40)
    surname = models.CharField(max_lenght=40)
    email = models.EmailField(max_length=100, unique=True)
    date_birth = models.DateField(blank=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_lenght=20)
    experience = models.IntegerField()
    description = models.TextField(max_lenght=500)

