from django.db import models

from courses.models import Course, Test


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    email = models.EmailField(max_length=100, unique=True)
    date_birth = models.DateField(blank=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)


class UserCourse(models.Model):
    date_start = models.DateTimeField()
    certified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='users')


class UserTest(models.Model):
    grade = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='users')
