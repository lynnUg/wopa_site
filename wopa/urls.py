from django.contrib import admin

admin.autodiscover()

from django.contrib.auth.views import login, logout
from django.conf.urls import *
from wopa_submitter import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'wopa.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^wopasite/', include('wopasite.urls')),
                       url(r'^website/', include('wopa_submitter.urls')),
                       url(r'^password-reset/',include('password_reset.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'login/',login,kwargs = {'template_name' : 'wopa_submitter/auth/login.html'}),
                      url(r'logout', logout,kwargs = {'template_name' : 'wopa_submitter/auth/login.html'}),
                       url(r'^$', views.index, name='assignments'),
                       
                       #url(r'^assignments/$', views.AssignmentsView.as_view(), name='assignments-index'),
                       #url(r'^login/$', views.user_login, name='login'),
                       #url(r'^logout/$', views.user_logout, name='logout'),
                       #url(r'^getsubmission/(\d+)/$', views.downloadSubmission, name='downloadSubmission'),  
                       #url(r'^getassignment/(\d+)/$', views.downloadAssignment, name='downloadAssignment'),  
                       #url(r'^createassignment/$', views.createAssignment, name='createAssignment'),
                       #url(r'^updateassignment/(\d+)/$', views.updateAssignment, name='updateAssignment'),
                       #url(r'^assignment/(\d+)/$', views.detailAssignment, name='viewAssignment'),
                       #url(r'^allAssignments$', views.allAssignments, name='allAssignments'),
                       #url(r'^submit/(\d+)/$', views.submitAssignment, name='submit'),
                       #url(r'^register/$', views.register, name='register'), 
                       #url(r'^createreading/$', views.createReading, name='createReading'),
                       url(r'^readings/$', views.getReadings, name='readings'),
                       #url(r'^getreadings/(\d+)/$', views.downloadReading, name='downloadReading'),
                       #url(r'^updatereading/(\d+)/$', views.updateReading, name='updateReading'),
                      #url(r'^forceSubmit/$', views.forceSubmitAssignment, name='forceSubmitAssignment'),
                       #url(r'^giveFeedback/$', views.giveFeedback, name='giveFeedback'),
                       # url(r'^submitFeedback/(\d+)/(\d+)/$', views.submitFeedback, name='submitFeedback'),
                      # url(r'^submissions/(\d+)/$', views.assignmentFeedback, name='assignmentFeedback'),
                      #url(r'^stats/$', views.statsStudents, name='stats'),
                      #url(r'^statsGraph/$', views.statsGraph, name='stats2'),
                      #url(r'^technicalInterview/$', views.technicalInterview, name='technicalInterview'),
                     # url(r'sendAssignmentEmail/$',views.sendAssignmentEmail, name='sendAssignmentEmail')
                      #url(r'^booking/', include('booking.urls')),
                       #url(r'^reservations/', include('reservations.urls')),
                       #(r'^booking/',TemplateView.as_view(template_name="wopa_submitter/wopainterviews/booking.html")),
                       


) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
