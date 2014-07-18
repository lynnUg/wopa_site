from django.db import models
from django.contrib.auth.models import User
#Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class Assignment(models.Model):
    name = models.CharField(max_length=128)
    about=models.TextField();
    sent=models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class StuAssign(models.Model):
    student = models.ForeignKey(User )
    assignment = models.ForeignKey(Assignment)
    marker=models.CharField(max_length=128)
    feedback=models.TextField()
    marked=models.BooleanField(default=False)
    documents = models.ForeignKey(Document,null=True)
    date_submitted = models.DateField()

