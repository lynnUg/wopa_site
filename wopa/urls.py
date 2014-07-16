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
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^createAssignment/$', views.createAssignment, name='createAssignment'), 
     url(r'^stuAssignment/$', views.stuAssignment, name='stuAssignment'), 
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^list/$', views.list, name='list'),
    url(r'^$', views.index, name='list'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
