from django.db import models
from django.contrib.auth.models import User
#Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    def __unicode__(self):
        return self.pk

class Assignment(models.Model):
    name = models.CharField(max_length=128)
    about=models.TextField();
    publish=models.BooleanField(default=False)
    def __unicode__(self):
        return self.pk
class Feedback(models.Model):
    thefeedback=models.TextField()
    marker=models.ForeignKey(User)
    def __unicode__(self):
        return self.pk

class StuAssign(models.Model):
    student = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    feedback=models.ForeignKey(Feedback,null=True)
    documents = models.ManyToManyField(Document,null=True)
    submitted=models.BooleanField(default=False)
    date_submitted = models.DateField(null=True)

