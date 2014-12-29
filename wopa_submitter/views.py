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
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
class UserCreateView(CreateView):
    template_name="wopa_submitter/auth/register.html"
    model = User
    fields = ['username']
    
        
    def post(self, request):
        context = RequestContext(request)
        user_form = UserForm(data=request.POST)
        invitation_code=request.POST['code']
        username = request.POST['username']
        password = request.POST['password']
        if user_form.is_valid() & (invitation_code=='@wopa256'):
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            self.assign_assignments_old(user)
            return HttpResponseRedirect('/website/register-success/')
        elif user_form.is_valid() & (invitation_code=='@wopa123'):
            user = user_form.save()
            user.set_password(user.password)
            user.is_staff=True
            user.save()
            return HttpResponseRedirect('/website/register-success/')
        elif  user_form.is_valid() & (invitation_code=='@wopaTemp'):
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            self.add_user_to_group(user)
            self.assign_assignments(user)
            return HttpResponseRedirect('/website/register-success/')
        else:
            if not((invitation_code=='@wopa123') or (invitation_code=='@wopa256')):
                invitation_code_error=True
        return render_to_response(
        'wopa_submitter/auth/register.html',
        {'user_form': user_form, 'user_errors': user_form.errors,'invitation_code_error':invitation_code_error},
        context)
    def add_user_to_group(self,user):
        g=Group.objects.get(name='wopaTemp')
        g.user_set.add(user)
    def assign_assignments(self,user):
        temp_assignments=Assignment.objects.filter(name="Technical Test")
        for assignment in temp_assignments:
            Submission.objects.create(student=user, assignment=assignment)
    def assign_assignments_old(self,user):
        published_assignments=Assignment.objects.filter(is_published=True)
        for assignment in published_assignments:
                Submission.objects.create(student=user, assignment=assignment)

class SubmissionListView(ListView):
    context_object_name = 'submissions'
    template_name = 'wopa_submitter/submissions/list.html'
    paginate_by = 10

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)
class ReadingListView(ListView):
    context_object_name="readings"
    template_name='wopa_submitter/readings/list.html'
    paginate_by=10
    model=Reading
class AssignmentListView(ListView):
    context_object_name="assignments"
    template_name='wopa_submitter/assignments/list.html'
    paginate_by=10
    model=Assignment

class ReadingCreateView(CreateView):
    template_name='wopa_submitter/readings/create.html'
    def get(self):
        reading_form = ReadingForm
        reading_document_form = ReadingDocumentForm
        return render_to_response('wopa_submitter/readings/create.html',
        {'reading_form': reading_form,'reading_document_form': reading_document_form,},context)
    def post(self):
        reading_form = ReadingForm(request.POST)
        reading_document_form=ReadingDocumentForm(request.POST,request.FILES)
        if reading_form.is_valid() & reading_document_form.is_valid():
            newreading =ReadingDocuments(docfile=request.FILES['docfile'])
            newreading.save()
            reading = reading_form.save()
            reading.reading=newreading
            reading.save()
            return HttpResponseRedirect('')

        return render_to_response('wopa_submitter/readings/create.html',
        {'reading_form': reading_form,'reading_document_form': reading_document_form,},context)  
    def sendReadingEmail(class_number,email):
    send_mail('Technical class '+class_number, "Hi ladies , \n Notes for technical class "+
        class_number+" are up on the site.Please visit the wopa website to view notes 'http://wopaoutbox.herokuapp.com/' \n\nRegards, \nLynn Asiimwe", 'lynnasiimwe@gmail.com', [email], fail_silently=False)
            


class AssignmentCreateView(CreateView):
    template_name='wopa_submitter/assignments.create.html'
    def get(self,request):
        context = RequestContext(request)
        assignment_form = AssignmentForm
        assignment_document_form = AssignmentDocumentForm
        return render_to_response('wopa_submitter/assignments/create.html',
        {'assignment_form': assignment_form,'assignment_document_form': assignment_document_form},context)
    def post(self,request):
        context = RequestContext(request)
        assignment_form = AssignmentForm(request.POST)
        assignment_document_form=AssignmentDocumentForm(request.POST,request.FILES)
        if assignment_form.is_valid() & assignment_document_form.is_valid():
            assignment = assignment_form.save()
            assignment.save()
            newdoc =AssignmentDocument(docfile=request.FILES['docfile'],assignment=assignment)
            newdoc.save()
            if assignment.is_published == True:
                for thegroup in assignment.groups.all():
                    self.assignAssignments(assignment,thegroup.name)
            return HttpResponseRedirect('')
        return render_to_response('wopa_submitter/assignments/create.html',
        {'assignment_form': assignment_form,'assignment_document_form': assignment_document_form, 
        'form_errors':assignment_form.errors},context)
    def assignAssignments(assignment,group_name):
     users = User.objects.filter(groups__name=group_name)
     for student in users:
            print "student "+ student.email
            Submission.objects.create(student=student, assignment=assignment)
            self.sendAssignmentEmail(assignment,student)

    def sendAssignmentEmail(assignment,user):
        name,class_number=assignment.name.split()
        send_mail('Technical class Reading and '+assignment.name, "Hi "+user.first_name+", \n Reading and Assignment for technical class "+
         class_number+" are up on the site.Please visit the wopa website to view class reading and assignment http://wopaoutbox.herokuapp.com/ \n\nP.S Assignment is compulsory and the readings is not \n\nRegards, \nLynn Asiimwe", 'lynnasiimwe@gmail.com', [user.email], fail_silently=False)

    

class ReadingUpdateView(CreateView):
    def get(self,request):
        context = RequestContext(request)
        eading = get_object_or_404(Reading, id=id)
        reading_form= ReadingForm(request.POST or None, instance=reading)
        reading_doc = get_object_or_404(ReadingDocuments,  pk=reading.reading.pk)
        reading_document_form=ReadingDocumentForm(request.POST or None,request.FILES or None,instance=reading_doc)
        return render_to_response('wopa_submitter/readings/update.html',
        {'reading_form': reading_form, 'reading_document_form': reading_document_form,'redirectPage':'/updatereading/'+id+'/'},
        context)
    def post(self,request):
        context = RequestContext(request)
        reading = get_object_or_404(Reading, id=id)
        reading_doc = get_object_or_404(ReadingDocuments, pk=reading.reading.pk)
        reading_form = ReadingForm(request.POST,instance=reading)
        reading_document_form=ReadingDocumentForm(request.POST,request.FILES,instance=reading_doc)
        if reading_form.is_valid() &reading_document_form.is_valid():
            reading= reading_form.save()
            reading_doc=reading_document_form.save()
        return render_to_response('wopa_submitter/readings/update.html',
        {'reading_form': reading_form, 'reading_document_form': reading_document_form,'redirectPage':'/updatereading/'+id+'/'},
        context)
                

class AssignmentUpdateView(CreateView):
    def get(self,request):
        context = RequestContext(request)
        assignment = get_object_or_404(Assignment, id=id)
        assignment_form= AssignmentForm(request.POST or None, instance=assignment)
        assignment_doc = get_object_or_404(AssignmentDocument, assignment=assignment.pk)
        assignment_document_form=AssignmentDocumentForm(request.POST or None,request.FILES or None,instance=assignment_doc)
        return render_to_response('wopa_submitter/assignments/update.html',
        {'assignment_form': assignment_form, 'assignment_document_form': assignment_document_form,'redirectPage':'/updateassignment/'+id+'/'},
        context)
    def post(self,request):
        context = RequestContext(request)
        assignment = get_object_or_404(Assignment, id=id)
        assignment_doc = get_object_or_404(AssignmentDocument, assignment=assignment.pk)
        assignment_form = AssignmentForm(request.POST,instance=assignment)
        assignment_document_form=AssignmentDocumentForm(request.POST,request.FILES,instance=assignment_doc)
        if assignment_form.is_valid() &assignment_document_form.is_valid():
            assignment= assignment_form.save()
            assignment_doc=assignment_document_form.save()
            if assignment_form.cleaned_data['is_published'] == True:
                for thegroup in assignment.groups.all():
                    self.assignAssignments(assignment,thegroup.name) 
                return HttpResponseRedirect('')
        return render_to_response('wopa_submitter/assignments/create.html',
        {'assignment_form': assignment_form, 'assignment_document_form': assignment_document_form,'redirectPage':'/updateassignment/'+id+'/'},
        context)
    def assignAssignments(assignment,group_name):
     users = User.objects.filter(groups__name=group_name)
     for student in users:
            print "student "+ student.email
            Submission.objects.create(student=student, assignment=assignment)
            self.sendAssignmentEmail(assignment,student)
    def sendAssignmentEmail(assignment,user):
        name,class_number=assignment.name.split()
        send_mail('Technical class Reading and '+assignment.name, "Hi "+user.first_name+", \n Reading and Assignment for technical class "+
         class_number+" are up on the site.Please visit the wopa website to view class reading and assignment http://wopaoutbox.herokuapp.com/ \n\nP.S Assignment is compulsory and the readings is not \n\nRegards, \nLynn Asiimwe", 'lynnasiimwe@gmail.com', [user.email], fail_silently=False)



@login_required
def home(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/website/student-account/')
    else:
        return HttpResponseRedirect('/website/staff-account/')
        






def detailAssignment(request,id):
    context = RequestContext(request)
    assignment=Assignment.objects.get(pk=id)
    submission_document_form=SubmissionDocumentForm()
    return render_to_response(
        'wopa_submitter/assignments/detail.html',
        {'assignment': assignment,'submission_document_form':submission_document_form},
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


   
@login_required
def downloadReading(request, id):

    # get the object by id or raise a 404 error
    object = get_object_or_404(ReadingDocuments, pk=id)

    return serve_file(request, object.docfile,save_as=True)

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
            sendFeedbackEmail(subs.assignment.name,subs.student.email)
            submitted="Feedback submitted"
    feedback_form = FeedbackForm()
    return render_to_response('wopa_submitter/feedback/create.html',
        {"submission":subs,"feedback_form":feedback_form,"submitted":submitted},context)

    


def sendFeedbackEmail(assignment,email):
    send_mail('Feedback on '+assignment, 'Hi Please visit the wopa website for feedback on '+assignment+" Please visit http://wopaoutbox.herokuapp.com/ to view feedback", 'lynnasiimwe@gmail.com', [email], fail_silently=False)

@staff_member_required
def technicalInterview(request):
    context = RequestContext(request)
    assignment= Assignment.objects.filter(name='Technical Test')
    submissions=Submission.objects.filter(assignment=assignment)
    #print len(submissions)
    filter_submission=[]
    for submission in submissions:
        if not(submission.student.first_name.lower()=="lynn" and submission.student.last_name.lower()=="asiimwe"):
            filter_submission.append(submission)


    return render_to_response('wopa_submitter/wopainterviews/index.html', {'submissionsTechnical': filter_submission}, context)
