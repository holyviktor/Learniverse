from django.db import models
from embed_video.fields import EmbedVideoField
from profiles.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)


class Course(models.Model):
    name = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_teacher')
    description = models.TextField(max_length=500)


class Module(models.Model):
    name = models.CharField(max_length=50, unique=True)
    duration = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')


class Lection(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)
    video = models.CharField(max_length=50, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lections')

    # def __iter__(self):
    #     for dish in self..all():
    #         yield dish

    # def __str__(self):
    #     return f'{self.title}'

    # class Meta:
    #     ordering = ('position', )


class Test(models.Model):
    title = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='tests')


class Question(models.Model):
    title = models.CharField(max_length=150)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')


class Answer(models.Model):
    title = models.CharField(max_length=50)
    correctness = models.BooleanField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')


class UserCourse(models.Model):
    date_start = models.DateTimeField()
    certified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='users')


class UserTest(models.Model):
    grade = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='users')

class Video(models.Model):
    title = models.CharField(max_length=200)
    video = EmbedVideoField()