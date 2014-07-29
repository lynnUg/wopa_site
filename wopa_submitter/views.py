from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView
from wopa_submitter.models import Reading, Assignment,Submission,AssignmentDocument
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from filetransfers.api import serve_file
from django.contrib.admin.views.decorators import staff_member_required
from wopa_submitter.forms import AssignmentForm,AssignmentDocumentForm,SubmissionDocumentForm,UserForm
import datetime

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
    assignmentsForUser = Submission.objects.filter(student=request.user)
    return render_to_response('wopa_submitter/index.html', {'assignmentsForUser': assignmentsForUser}, context)





def register(request):
    context = RequestContext(request)
    registered = False
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
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render_to_response(
        'wopa_submitter/auth/index.html',
        {'user_form': user_form, 'user_errors': user_form.errors, 'registered': registered},
        context)

def assignAssignments(assignment):
     users = User.objects.all()
     for student in users:
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


    return render_to_response('wopa_submitter/assignments/index.html',
        {'assignment_form': assignment_form,'assignment_document_form': assignment_document_form, 'created': created},context)


def detailAssignment(request,id):
    context = RequestContext(request)
    assignment=Assignment.objects.get(pk=id)
    submission_document_form=SubmissionDocumentForm()
    created=True
    return render_to_response(
        'wopa_submitter/assignments/index.html',
        {'assignment': assignment,'submission_document_form':submission_document_form, 'created': created},
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
        
    
    return render_to_response('wopa_submitter/assignments/index.html',
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
            if submission.submissions.count()<10:
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
    return render_to_response('wopa_submitter/assignments/index.html',
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
class ReadingView(TemplateView, LoginRequiredMixin):
    template_name = "wopa_submitter/readings/index.html"
    model = Reading
    context_object_name = 'readings'


class AssignmentsView(ListView, LoginRequiredMixin):
    template_name = "wopa_submitter/assignments/index.html"
    model = Assignment
    context_object_name = "assignments"
