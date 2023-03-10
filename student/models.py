from django.db import models

from courses.models import Course


# Create your models here.
class User(models.Model):
    name = models.CharField(max_lenght=40)
    surname = models.CharField(max_lenght=40)
    email = models.EmailField(max_length=100, unique=True)
    date_birth = models.DateField(blank=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_lenght=20)


class UserCourse(models.Model):
    date_start = models.DateTimeField()
    certified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='users')
