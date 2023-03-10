from django.db import models


# Create your models here.
class Lection(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)
    video = models.CharField(max_length=50, blank=True)

    # def __iter__(self):
    #     for dish in self..all():
    #         yield dish

    def __str__(self):
        return f'{self.title}'

    # class Meta:
    #     ordering = ('position', )


class Module(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # lection = models.ForeignKey(Lection, on_delete=models.CASCADE, related_name='dishes')
    duration = models.TimeField()


class Course(models.Model):
    name = models.CharField(max_length = 50)
    duration = models.TimeField()
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(max_length=500)


class Test(models.Model):
    title = models.CharField(max_length=100)


class Question(models.Model):
    title = models.CharField(max_length=150)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')


class Answer(models.Model):
    title = models.CharField(max_length=50)
    correctness = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')