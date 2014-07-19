from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    def __unicode__(self):
        return self.pk


class Assignment(models.Model):
    name = models.CharField(max_length=128)
    about = models.TextField()
    details = models.TextField()
    is_published = models.BooleanField(default=False)
    assignment_file = models.FileField(upload_to="assignments/%Y/%m/%d")
    due_date = models.DateField()

    def __unicode__(self):
        return self.name


class Feedback(models.Model):
    thefeedback = models.TextField()
    marker = models.ForeignKey(User)

    def __unicode__(self):
        return self.pk


class Submission(models.Model):
    student = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    feedback = models.ForeignKey(Feedback, null=True)
    documents = models.ManyToManyField(Document, null=True)
    submitted = models.BooleanField(default=False)
    date_submitted = models.DateField(null=True)


class Reading(models.Model):
    name = models.CharField(max_length=250)
    file = models.FileField(upload_to="readings/%Y/%m/%d")
    message = models.TextField()



