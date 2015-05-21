from django.conf.urls import patterns, url, include

from .views import item_view_set


urlpatterns = patterns(
    '',
    url(r'^base_template$', 'sampleapp.views.base_template', name='base_template'),

    url(r'^list_header$', 'sampleapp.views.list_header', name='list_header'),
    url(r'^list_col$', 'sampleapp.views.list_col', name='list_col'),
    url(r'^list_col_head$',
        'sampleapp.views.list_col_head', name='list_col_head'),
    url(r'^list_sql$', 'sampleapp.views.list_sql', name='list_sql'),

    url(r'^item/add_tab$', 'sampleapp.views.item_add_tab', name='add_tab'),
    url(r'^item/add_accordion$', 'sampleapp.views.item_add_accordion', name='add_accordion'),
    url(r'^item/(?P<pk>\d+)/detail_tab$', 'sampleapp.views.item_detail_tab', name='detail_tab'),
    url(r'^item/(?P<pk>\d+)/detail_accordion$', 'sampleapp.views.item_detail_accordion', name='detail_accordion'),
    url(r'^item/upload$', 'sampleapp.views.item_upload', name='upload'),
    url(r'^item/', include(item_view_set.urls)),

    url(r'^permission_01$', 'sampleapp.views.permission_01', name='permission_01'),
    url(r'^permission_02$', 'sampleapp.views.permission_02', name='permission_02'),
    url(r'^permission_filter$', 'django.shortcuts.render',
        {'template_name': 'permission_filter.html'}, name='permission_filter'),
)
