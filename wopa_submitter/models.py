from django.db import models
from django.contrib.auth.models import User
#Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class Assignment(models.Model):
    name = models.CharField(max_length=128)
    about=models.TextField();
    publish=models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
class Feedback(models.Model):
    thefeedback=models.TextField()
    marker=models.ForeignKey(User)

class StuAssign(models.Model):
    student = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    marker=models.CharField(max_length=128,null=True)
    feedback=models.ForeignKey(Feedback)
    marked=models.BooleanField(default=False)
    documents = models.ForeignKey(Document,null=True)
    submitted=models.BooleanField(default=False)
    date_submitted = models.DateField(null=True)

