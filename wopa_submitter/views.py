from django.shortcuts import render
from wopa_submitter.forms import UserForm, DocumentForm, AssignmentForm, StuAssignmentForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from wopa_submitter.models import Document, Submission
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def user_login(request):
    # Like before, obtain the context for the user's request.
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

    return render_to_response('wopa-submitter/login.html',
                              {'account_diasbled': account_diasbled, 'invalid_account': invalid_account,
                               'username': username, 'password': password}, context)


@login_required
def user_logout(request):
    print "in logout"
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def index(request):
    # print "in index"
    context = RequestContext(request)
    assignmentsForUser = Submission.objects.filter(student=request.user)
    return render_to_response('wopa-submitter/index.html', {'assignmentsForUser': assignmentsForUser}, context)


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('wopa_submitter.views.list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'wopa-submitter/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render_to_response(
        'wopa-submitter/login.html',
        {'user_form': user_form, 'user_errors': user_form.errors, 'registered': registered},
        context)


def createAssignment(request):
    # Like before, get the request's context.   
    context = RequestContext(request)
    created = False;
    if request.method == 'POST':
        assignment_form = AssignmentForm(data=request.POST)

        if assignment_form.is_valid():
            assignment = assignment_form.save()
            print "in create assignment"
            assignment.save()
            if assignment.publish == True:
                users = User.objects.all()
                for student in users:
                    assigntoStu = Submission.objects.create(student=student, assignment=assignment)
            created = True;

        else:
            print assignment_form.errors
    else:
        assignment_form = AssignmentForm

    return render_to_response(
        'wopa-submitter/assignment.html',
        {'assignment_form': assignment_form, 'created': created},
        context)


def stuAssignment(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    created = False;
    if request.method == 'POST':
        stuAssignment_form = StuAssignmentForm(data=request.POST)

        if stuAssignment_form.is_valid():
            stuAssignment = stuAssignment_form.save()
            print "in create assignment"
            stuAssignment.save()
            created = True;

        else:
            print stuAssignment_form.errors
    else:
        stuAssignment_form = StuAssignmentForm

    return render_to_response(
        'wopa-submitter/stuassign.html',
        {'stuAssignment_form': stuAssignment_form, 'created': created},
        context)