from django.contrib.auth.models import User
from django import forms
from wopa_submitter.models import Document, Assignment, Submission


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

    class Meta:
        model = Document


class AssignmentForm(forms.ModelForm):
    name = forms.CharField()
    about = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Assignment
        fields = ('name', 'about', 'is_published')


class StuAssignmentForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('student', 'assignment')