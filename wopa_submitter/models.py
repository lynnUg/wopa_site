from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):
    name = models.CharField(max_length=128)
    about = models.TextField()
    details = models.TextField()
    is_published = models.BooleanField(default=False)
    due_date = models.DateField()
    file = models.FileField(upload_to="assignments/%Y/%m/%d")

    def __unicode__(self):
        return self.name



class Feedback(models.Model):
    thefeedback = models.TextField()
    marker = models.ForeignKey(User)

    def __unicode__(self):
        return self.pk


def submissionfile(self,filename):
    url = "submissions/students/%s/%s" % (self.submitter.username,filename)
    return url

class SubmissionDocument(models.Model):
    submitter=models.ForeignKey(User)
    docfile = models.FileField(upload_to=submissionfile)


class Submission(models.Model):
    student = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    feeling_about_assignment = models.TextField()
    feedback = models.ForeignKey(Feedback, null=True)
    submitted = models.BooleanField(default=False)
    date_submitted = models.DateField(null=True)
    file = models.FileField(upload_to="submissions/%Y/%m/%d")


class Reading(models.Model):
    name = models.CharField(max_length=250)
    message = models.TextField()
    document = models.FileField(upload_to="readings/%Y/%m/%d")


    def __unicode__(self):
        return self.name

class ReadingDocument(models.Model):
    docfile = models.FileField(upload_to='readings')
    



class AssignmentDocument(models.Model):
    assignment = models.OneToOneField(Assignment,null=True)
    docfile = models.FileField(upload_to='assignments')


