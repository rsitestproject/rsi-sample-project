
from django.conf.urls import patterns, include, url, static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from rsi.menubar.menu import menubar
menubar.load()

urlpatterns = patterns(
    '',
    url(r'', include('rsi.dashboard.urls', namespace='dashboard')),
    url(r'', include('rsi.auth_ext.urls', namespace='auth_ext')),
    url(r'', include('rsi.azure.auth_urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('sampleapp.urls', namespace='sampleapp')),
    url(r'', include('sampleapp2.urls', namespace='sampleapp2')),
    url(r'', include('sampleapp3.urls', namespace='sampleapp3')),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
