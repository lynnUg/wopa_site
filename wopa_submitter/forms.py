from django.contrib.auth.models import User
from django import forms

from wopa_submitter.models import Assignment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class AssignmentForm(forms.ModelForm):
    name = forms.CharField()
    about = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Assignment
        fields = ('name', 'about', 'is_published','due_date')


