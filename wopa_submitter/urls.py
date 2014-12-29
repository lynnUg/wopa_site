from django.conf.urls import patterns, include, url

from views import UserCreateView,SubmissionListView,ReadingListView,home,AssignmentListView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
user_create_view = UserCreateView.as_view()
submission_list_view=SubmissionListView.as_view()
reading_list_view=ReadingListView.as_view()
assignment_list_view=AssignmentListView.as_view()
urlpatterns = patterns('',
   url(r'^register/$', user_create_view),
   url(r'^register-success/$', TemplateView.as_view(template_name='wopa_submitter/foo.html')),
   url(r'^student-account/$', login_required(submission_list_view),name='submissions'),
   url(r'^staff-account/$', login_required(assignment_list_view),name='assignments'),
   url(r'^readings/$',login_required(reading_list_view) , name='readings'),
   url(r'^home/$',home )
   
)