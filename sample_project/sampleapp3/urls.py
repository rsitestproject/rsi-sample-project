from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns(
    '',
    url(r'^document_file2/', include(views.document_file_viewset.urls)),
    url(r'^document_file2/(?P<pk>\d+)/download/$', views.document_file_download_file_view, name='document_file_download'),
    url(r'^aad_userlist/', 'sampleapp3.views.aad_userlist', name='aad_userlist'),
)
