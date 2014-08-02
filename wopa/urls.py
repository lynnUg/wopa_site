from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static

import wopa_submitter.views as views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'wopa.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.index, name='assignments'),
                       
                       #url(r'^assignments/$', views.AssignmentsView.as_view(), name='assignments-index'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^getsubmission/(\d+)/$', views.downloadSubmission, name='downloadSubmission'),  
                       url(r'^getassignment/(\d+)/$', views.downloadAssignment, name='downloadAssignment'),  
                       url(r'^createassignment/$', views.createAssignment, name='createAssignment'),
                       url(r'^updateassignment/(\d+)/$', views.updateAssignment, name='updateAssignment'),
                       url(r'^assignment/(\d+)/$', views.detailAssignment, name='viewAssignment'),
                       url(r'^allAssignments$', views.allAssignments, name='allAssignments'),
                       url(r'^submit/(\d+)/$', views.submitAssignment, name='submit'),
                       url(r'^register/$', views.register, name='register'), 
                       url(r'^createreading/$', views.createReading, name='createReading'),
                       url(r'^readings/$', views.getReadings, name='readings'),
                       url(r'^getreadings/(\d+)/$', views.downloadReading, name='downloadReading'),
                       url(r'^updatereading/(\d+)/$', views.updateReading, name='updateReading'),


) 
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
