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
                       url(r'^register/$', views.register, name='register'),  # ADD NEW PATTERN!
                       url(r'^createassignment/$', views.createAssignment, name='create'),
                       url(r'^assignment/(\d+)/$', views.detailAssignment, name='viewAssignment'),
                       url(r'^updateassignment/(\d+)/$', views.updateAssignment, name='update'),
                       url(r'^getsubmission/(\d+)/$', views.downloadSubmission, name='downloadSubmission'),  
                       url(r'^getassignment/(\d+)/$', views.downloadAssignment, name='downloadAssignment'),  
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^submit/(\d+)/$', views.submitAssignment, name='logout'),
                       url(r'^readings/$', views.Reading.as_view(), name='reading'),
                       url(r'^assignments/$', views.index, name='assignments'),
                       url(r'^$', views.index, name='index'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
