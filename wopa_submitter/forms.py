from django.contrib.auth.models import User
from django import forms

from wopa_submitter.models import Assignment ,AssignmentDocument,SubmissionDocument,ReadingDocuments,Reading

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


class AssignmentDocumentForm(forms.ModelForm):
  docfile = forms.FileField(label='Select a file',help_text='')
  class Meta:
    model = AssignmentDocument
    exclude=('assignment',)
class SubmissionDocumentForm(forms.ModelForm):
    docfile = forms.FileField(
           label='Select a file',
                  help_text='max. 42 megabytes'
                      )    
    class Meta:
            model = SubmissionDocument
            exclude=('submitter','filename')
class ReadingForm(forms.ModelForm):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Reading
        fields = ('name', 'message', )


class ReadingDocumentForm(forms.ModelForm):
  docfile = forms.FileField(label='Select a file',help_text='')
  class Meta:
    model = ReadingDocuments

 