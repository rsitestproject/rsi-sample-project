from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns(
    '',
    url(r'^item2/', include('sampleapp2.item_urls', namespace='item2')),
    url(r'^category/', include(views.category_viewset.urls)),
    url(r'^document_file/', include(views.document_file_viewset.urls)),
    url(r'^document_file/(?P<pk>\d+)/download/$', views.document_file_download_file_view, name='document_file_download'),
    url(r'^entry/$', views.entry_list_sql_view, name='entry_list_sql'),
    url(r'^tag/', include(views.tag_viewset.urls)),
)
