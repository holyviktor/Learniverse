from django.contrib import admin
from .models import Course, Category, Module, Lection, Test, Question, Answer

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Module)
admin.site.register(Lection)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
