from django.db import models

from teacher.models import Teacher


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)


class Course(models.Model):
    name = models.CharField(max_length=50)
    duration = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    description = models.IntegerField(max_length=500)


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

    def __str__(self):
        return f'{self.title}'

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
    correctness = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')