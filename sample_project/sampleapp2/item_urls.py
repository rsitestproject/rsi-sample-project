from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^create$', 'sampleapp2.views.create', name='create'),
    url(r'^$', 'sampleapp2.views.list', name='list'),
    url(r'^sidebar$', 'sampleapp2.views.list_sidebar', name='list_sidebar'),
    url(r'^(?P<pk>\d+)/update$', 'sampleapp2.views.update', name='update'),
    url(r'^(?P<pk>\d+)/delete$', 'sampleapp2.views.delete', name='delete'),
    url(r'^(?P<pk>\d+)/$', 'sampleapp2.views.detail', name='detail'),
)
