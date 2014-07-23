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
                       url(r'^$', views.Index.as_view(), name='index'),
                       url(r'^readings/$', views.ReadingView.as_view(), name='readings'),
                       url(r'^assignments/$', views.AssignmentsView.as_view(), name='assignments-index'),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
