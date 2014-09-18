from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView
from wopa_submitter.models import Reading, Assignment,Submission,AssignmentDocument,SubmissionDocument,ReadingDocuments,Feedback
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from filetransfers.api import serve_file
from django.contrib.admin.views.decorators import staff_member_required
from wopa_submitter.forms import AssignmentForm,AssignmentDocumentForm,SubmissionDocumentForm,UserForm,ReadingForm,ReadingDocumentForm,SubmissionForm,FeedbackForm
from django.contrib.auth.models import User
import datetime
from django.utils import simplejson
from django.core.mail import send_mail
from django import template


def user_login(request):
    context = RequestContext(request)
    account_diasbled = False
    invalid_account = False
    username = ''
    password = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                print "logged in"
                return HttpResponseRedirect('/')
            else:
                # return HttpResponse("Your WOPA account is disabled.")
                account_diasbled = True
                invalid_account = True

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            invalid_account = True
            # return HttpResponse("Invalid login details supplied.")

    return render_to_response('wopa_submitter/auth/index.html',
                              {'account_diasbled': account_diasbled, 'invalid_account': invalid_account,
                               'username': username, 'password': password}, context)


@login_required
def user_logout(request):
    print "in logout"
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def index(request):
    context = RequestContext(request)
    group = Group.objects.get(name='wopaTemp')
    if not request.user.is_staff:
        assignmentsForUser = Submission.objects.filter(student=request.user)
        return render_to_response('wopa_submitter/assignments/index.html', {'assignmentsForUser': assignmentsForUser}, context)
    elif group in request.user.groups.all():
        assignmentsForUser = Submission.objects.filter(student=request.user)
        return render_to_response('wopa_submitter/assignments/index.html', {'assignmentsForUser': assignmentsForUser}, context)
    else:
        return allAssignments(request)


def register(request):
    context = RequestContext(request)
    registered = False
    invitation_code_error=False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        invitation_code=request.POST['code']
        username = request.POST['username']
        password = request.POST['password']
        print invitation_code
        if user_form.is_valid() & (invitation_code=='@wopa256'):
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            published_assignments=Assignment.objects.filter(is_published=True)
            for assignment in published_assignments:
                Submission.objects.create(student=user, assignment=assignment)
            the_user = authenticate(username=username, password=password)
            login(request, the_user)
            return HttpResponseRedirect('/')
        elif user_form.is_valid() & (invitation_code=='@wopa123'):
            user = user_form.save()
            user.set_password(user.password)
            user.is_staff=True
            user.save()
            registered = True
            the_user = authenticate(username=username, password=password)
            login(request, the_user)
            return HttpResponseRedirect('/')
        elif  user_form.is_valid() & (invitation_code=='@wopaTemp'):
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            g = Group.objects.get(name='wopaTemp')
            g.user_set.add(user)
            registered = True
            temp_assignments=Assignment.objects.filter(name="Technical Test")
            for assignment in temp_assignments:
                Submission.objects.create(student=user, assignment=assignment)
            the_user = authenticate(username=username, password=password)
            login(request, the_user)
            return HttpResponseRedirect('/')
        else:
            if not((invitation_code=='@wopa123') or (invitation_code=='@wopa256')):
                invitation_code_error=True


            print user_form.errors
    else:
        user_form = UserForm()

    return render_to_response(
        'wopa_submitter/auth/index.html',
        {'user_form': user_form, 'user_errors': user_form.errors, 'registered': registered,'invitation_code_error':invitation_code_error},
        context)

def assignAssignments(assignment):
     users = User.objects.all()
     for student in users:
        if not student.is_staff:
            Submission.objects.create(student=student, assignment=assignment)
@staff_member_required
def createAssignment(request):   
    context = RequestContext(request)
    created = False;
    if request.method == 'POST':
        assignment_form = AssignmentForm(request.POST)
        assignment_document_form=AssignmentDocumentForm(request.POST,request.FILES)
        if assignment_form.is_valid() & assignment_document_form.is_valid():
            assignment = assignment_form.save()
            assignment.save()
            newdoc =AssignmentDocument(docfile=request.FILES['docfile'],assignment=assignment)
            newdoc.save()
            #print AssignmentDocument.objects.all()
            if assignment.is_published == True:
                assignAssignments(assignment)
            created = True;

        else:
            print assignment_form.errors
    else:
        assignment_form = AssignmentForm
        assignment_document_form = AssignmentDocumentForm


    return render_to_response('wopa_submitter/assignments/create.html',
        {'assignment_form': assignment_form,'assignment_document_form': assignment_document_form, 'created': created},context)


def detailAssignment(request,id):
    context = RequestContext(request)
    assignment=Assignment.objects.get(pk=id)
    submission_document_form=SubmissionDocumentForm()
    return render_to_response(
        'wopa_submitter/assignments/detail.html',
        {'assignment': assignment,'submission_document_form':submission_document_form},
        context)
@staff_member_required
def updateAssignment(request,id):
    context = RequestContext(request)
    created=False
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, id=id)
        assignment_doc = get_object_or_404(AssignmentDocument, assignment=assignment.pk)
        assignment_form = AssignmentForm(request.POST,instance=assignment)
        assignment_document_form=AssignmentDocumentForm(request.POST,request.FILES,instance=assignment_doc)
        if assignment_form.is_valid() &assignment_document_form.is_valid():
            assignment= assignment_form.save()
            assignment_doc=assignment_document_form.save()
            
            if assignment_form.cleaned_data['is_published'] == True:
                 submissions=Submission.objects.filter(assignment=assignment)
                 if len(submissions)<=0:
                    assignAssignments(assignment)
            created=True

        else:
            print assignment_form.errors
    else:
        assignment = get_object_or_404(Assignment, id=id)
        print assignment.pk
        assignment_form= AssignmentForm(request.POST or None, instance=assignment)
        assignment_doc = get_object_or_404(AssignmentDocument, assignment=assignment.pk)
        assignment_document_form=AssignmentDocumentForm(request.POST or None,request.FILES or None,instance=assignment_doc)
        
    
    return render_to_response('wopa_submitter/assignments/create.html',
        {'assignment_form': assignment_form, 'assignment_document_form': assignment_document_form,'created': created,'redirectPage':'/updateassignment/'+id+'/'},
        context)
@login_required
def submitAssignment(request,id):
    context = RequestContext(request)
    created = True;
    assignment=get_object_or_404(Assignment,pk=id)
    if request.method == 'POST':
        submission_document_form=SubmissionDocumentForm(request.POST,request.FILES)
        if submission_document_form.is_valid():
            submission=get_object_or_404(Submission,assignment=assignment.pk ,student=request.user.pk)
            newdoc =SubmissionDocument(docfile=request.FILES['docfile'],submitter=request.user)
            newdoc.save()
            if submission.submissions.count()<4:
                submission.submissions.add(newdoc)
                submission.submitted=True
                submission.date_submitted=datetime.datetime.now()
                submission.save()
            return HttpResponseRedirect('/')

        else:
            print submission_document_form.errors
    else:
        submission_document_form=SubmissionDocumentForm()
        #assignment_form = AssignmentForm
    return render_to_response('wopa_submitter/assignments/detail.html',
        {'submission_document_form': submission_document_form,'assignment': assignment,'created': created ,'submission_document_form.errors':submission_document_form.errors},context)
@login_required
def downloadSubmission(request, id):

    # get the object by id or raise a 404 error
    object = get_object_or_404(SubmissionDocument, pk=id)

    return serve_file(request, object.docfile,save_as=True)
@login_required
def downloadAssignment(request, id):

    # get the object by id or raise a 404 error
    object = get_object_or_404(AssignmentDocument, pk=id)

    return serve_file(request, object.docfile,save_as=True)
@staff_member_required
def createReading(request): 
    context = RequestContext(request)
    created = False;
    if request.method == 'POST':
        reading_form = ReadingForm(request.POST)
        reading_document_form=ReadingDocumentForm(request.POST,request.FILES)
        if reading_form.is_valid() & reading_document_form.is_valid():
            newreading =ReadingDocuments(docfile=request.FILES['docfile'])
            newreading.save()
            reading = reading_form.save()
            reading.reading=newreading
            reading.save()
            
            #print AssignmentDocument.objects.all()
            created = True;

        else:
            print assignment_form.errors
    else:
        reading_form = ReadingForm
        reading_document_form = ReadingDocumentForm


    return render_to_response('wopa_submitter/readings/create.html',
        {'reading_form': reading_form,'reading_document_form': reading_document_form, 'created': created},context)  
@login_required
def getReadings(request):
    context = RequestContext(request)
    if not request.user.is_staff:
        readings = Reading.objects.all()
        return render_to_response('wopa_submitter/readings/index.html', {'readings': readings}, context)
    else:
        readings = Reading.objects.all()
        return render_to_response('wopa_submitter/readings/list.html', {'readings': readings}, context)
@login_required
def downloadReading(request, id):

    # get the object by id or raise a 404 error
    object = get_object_or_404(ReadingDocuments, pk=id)

    return serve_file(request, object.docfile,save_as=True)
@staff_member_required
def allAssignments(request):
    context = RequestContext(request)
    assignments= Assignment.objects.all()
    return render_to_response('wopa_submitter/assignments/list.html', {'assignments': assignments}, context)
@staff_member_required
def updateReading(request,id):
    context = RequestContext(request)
    created=False
    if request.method == 'POST':
        reading = get_object_or_404(Reading, id=id)
        reading_doc = get_object_or_404(ReadingDocuments, pk=reading.reading.pk)
        reading_form = ReadingForm(request.POST,instance=reading)
        reading_document_form=ReadingDocumentForm(request.POST,request.FILES,instance=reading_doc)
        if reading_form.is_valid() &reading_document_form.is_valid():
            reading= reading_form.save()
            reading_doc=reading_document_form.save()
            
            created=True

        else:
            print reading_form.errors
    else:
        reading = get_object_or_404(Reading, id=id)
        reading_form= ReadingForm(request.POST or None, instance=reading)
        reading_doc = get_object_or_404(ReadingDocuments,  pk=reading.reading.pk)
        reading_document_form=ReadingDocumentForm(request.POST or None,request.FILES or None,instance=reading_doc)

    return render_to_response('wopa_submitter/readings/create.html',
        {'reading_form': reading_form, 'reading_document_form': reading_document_form,'created': created,'redirectPage':'/updatereading/'+id+'/'},
        context)
        
@staff_member_required
def forceSubmitAssignment(request):
    context = RequestContext(request)
    created = True;
    #assignment=get_object_or_404(Assignment,pk=id)
    submission=SubmissionForm()
    submission_document_form=SubmissionDocumentForm()
    if request.method == 'POST':
        submission_document_form=SubmissionDocumentForm(request.POST,request.FILES)
        if submission_document_form.is_valid():
            #print request.POST['assignment'], request.POST['student']
            submission=get_object_or_404(Submission,assignment=request.POST['assignment'] ,student=request.POST['student'])
            newdoc =SubmissionDocument(docfile=request.FILES['docfile'],submitter=request.user)
            newdoc.save()
            if submission.submissions.count()<10:
                submission.submissions.add(newdoc)
                submission.submitted=True
                submission.date_submitted=datetime.datetime.now()
                submission.save()
            return HttpResponseRedirect('/forceSubmit/')
        

        else:
            print submission_document_form.errors
    else:
        submission=SubmissionForm()
        submission_document_form=SubmissionDocumentForm()
        #assignment_form = AssignmentForm
    return render_to_response('wopa_submitter/assignments/forceSubmit.html',
        {'submission_document_form': submission_document_form,'form': submission,'created': created },context)
@staff_member_required
def statsStudents(request):
    context = RequestContext(request)
    users= User.objects.filter(is_staff=False,is_active=True)
    assignments=[i.name for i in Assignment.objects.filter(is_published=True).order_by('name')]
    the_users=[]
    for user in users:
        user_submission=[user.first_name]
        submissions=Submission.objects.filter(student=user).order_by('assignment')
        for submission in submissions:
            user_submission.append(submission.submitted)
        the_users.append(user_submission)
   
    return render_to_response('wopa_submitter/assignments/breakdown.html',
        {'the_users': the_users,'assignments': assignments,},context)
@login_required
def statsGraph(request):
    context=RequestContext(request)
    assignments= Assignment.objects.filter(is_published=True).order_by('name')
    output=[]
    for assignment in assignments:
        assD={}
        sub=Submission.objects.filter(assignment=assignment,submitted=True,student__is_staff=False)
        assD["a"]=len(sub)
        assD["y"]=assignment.name
        output.append(assD)
    entry = simplejson.dumps(output)
    return render_to_response('wopa_submitter/assignments/graph.html',
        {"entry":entry},context)
def giveFeedback(request):
    context=RequestContext(request)
    assignments=Assignment.objects.filter(is_published=True).order_by('name')
    return render_to_response('wopa_submitter/feedback/assignmentlist.html',
        {"assignments":assignments},context)
    #pass
def assignmentFeedback(request,assignment_id):
    context=RequestContext(request)
    subs=Submission.objects.filter(assignment=assignment_id,submitted=True,student__is_staff=False)
    return render_to_response('wopa_submitter/feedback/submissionlist.html',
        {"student_submissions":subs},context)
def submitFeedback(request,student_id,assignment_id):
    context=RequestContext(request)
    subs=Submission.objects.filter(assignment=assignment_id,student=student_id,submitted=True,student__is_staff=False)
    #print len(subs),"number of submission
    submitted=""
    if subs:
        subs= subs[0]
    else:
        subs=None
    if request.method == 'POST' and subs.feedback==None:
        feedback_form=FeedbackForm(request.POST,request.FILES)
        if feedback_form.is_valid():
            feedback=feedback_form.save(commit=False)
            feedback.marker=request.user
            feedback.save()
            subs.feedback=feedback
            subs.save()
            sendAssignmentEmail(subs.assignment.name,subs.student.email)
            submitted="Feedback submitted"
    feedback_form = FeedbackForm()
    return render_to_response('wopa_submitter/feedback/create.html',
        {"submission":subs,"feedback_form":feedback_form,"submitted":submitted},context)
def sendAssignmentEmail(assignment,email):
    send_mail('Feedback on '+assignment, 'Hi Please visit the wopa website for feedback on '+assignment+" Please visit 'http://wopaoutbox.herokuapp.com/' to view feedback", 'lynnasiimwe@gmail.com', [email], fail_silently=False)


class ReadingView(ListView, LoginRequiredMixin):
    template_name = "wopa_submitter/readings/index.html"
    model = Reading
    context_object_name = 'readings'


class AssignmentsView(ListView, LoginRequiredMixin):
    template_name = "wopa_submitter/assignments/index.html"
    model = Assignment
    context_object_name = "assignments"
