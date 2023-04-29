from django import forms

from courses.models import UserCourse, Answer, Question


class EnrollForm(forms.Form):
    class Meta:
        model = UserCourse
        fields = ('course_enroll')

    course_enroll = forms.CharField(widget=forms.HiddenInput(attrs={'name': "course_enroll"}))
    # course_delete = forms.CharField(widget=forms.HiddenInput(attrs={'name': "course_delete"}))


class DeleteForm(forms.Form):
    class Meta:
        model = UserCourse
        fields = ('course_delete')

    course_delete = forms.CharField(widget=forms.HiddenInput(attrs={'name': "course_delete"}))


class TestForm(forms.Form):
    class Meta:
        model = Answer, Question
        fields = 'answer'

    answer = []

