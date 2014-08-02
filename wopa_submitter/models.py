from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Assignment(models.Model):
    name = models.CharField(max_length=128)
    about = models.TextField()
    details = models.TextField()
    is_published = models.BooleanField(default=False)
    due_date = models.DateField()

    


class Feedback(models.Model):
    thefeedback = models.TextField()
    marker = models.ForeignKey(User)

    def __unicode__(self):
        return self.pk

def submissionfile(self,filename):
    #print filename
    #self.filename=filename
    url = "submissions/students/%s/%s" % (self.submitter.username,filename)
    return url

class SubmissionDocument(models.Model):
    submitter=models.ForeignKey(User)
    #filename=models.CharField(max_length=128)
    docfile = models.FileField(upload_to=submissionfile)


class Submission(models.Model):
    student = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    feedback = models.ForeignKey(Feedback, null=True)
    submitted = models.BooleanField(default=False)
    date_submitted = models.DateField(null=True)
    submissions= models.ManyToManyField(SubmissionDocument,null=True)

class ReadingDocuments(models.Model):
    docfile = models.FileField(upload_to='readings')

    def __unicode__(self):
        return self.pk

class Reading(models.Model):
    name = models.CharField(max_length=250)
    message = models.TextField()
    reading=models.ForeignKey(ReadingDocuments,null=True)

class AssignmentDocument(models.Model):
    assignment = models.OneToOneField(Assignment,null=True)
    docfile = models.FileField(upload_to='assignments')


