# coding: utf-8
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.db import models as django_models
from django import forms as django_forms
from django.shortcuts import render

from rsi.common.views.list import ListView, SQLListView
from rsi.common.views.edit import (
    CreateAndDuplicateView, UpdateView, DeleteView, InlineEdit)
from rsi.common.views.detail import (
    DetailView)
from rsi.common.views import viewset
from rsi.common.search import types
from rsi.common.files import views as files_views
from rsi.role import api as role_api

from . import models
from . import forms


class DocumentFileInlineEdit(InlineEdit):
    label = _('Document file')
    model = models.DocumentFile
    override_params = {
        'extra': 2,
    }


class ItemList(ListView):
    model = models.Item2
    list_display = ['name']
    template_name = 'common/list/list.html'
    search_fields = (
        ('name', types.TEXT_WILDCARD),
        ('categories', types.CHECKBOX_MULTIPLE),
    )

list = ItemList.as_view()


class ItemListSidebar(ListView):
    model = models.Item2
    list_display = ['name']
    template_name = 'common/list/list.html'
    search_type = 'sidebar'
    search_sidebar = {
        'filter': [
            ('categories', types.SELECT_SIDEBAR_MULTIPLE),
        ],
        'freetext': [
            'name',
        ]
    }

list_sidebar = ItemListSidebar.as_view()

class ItemDelete(DeleteView):
    model = models.Item2
    form_class = forms.ItemForm
    success_url = reverse_lazy('sampleapp2:item2:list')
    inlines = [DocumentFileInlineEdit]
    fieldsets = [
        (None, {'fields': ['name', 'price']}),
        (_('Option'), {'fields': ['enabled', 'categories']}),
    ]

delete = ItemDelete.as_view()


class ItemUpdate(UpdateView):
    model = models.Item2
    form_class = forms.ItemForm
    success_url = reverse_lazy('sampleapp2:item2:list')
    inlines = [DocumentFileInlineEdit]
    template_name = 'sampleapp2/custom.html'
    fieldsets = [
        (None, {'fields': ['name', 'price']}),
        (_('Option'), {'fields': ['enabled', 'categories']}),
    ]

update = ItemUpdate.as_view()


class ItemDetail(DetailView):
    model = models.Item2
    form_class = forms.ItemForm
    inlines = [DocumentFileInlineEdit]
    fieldsets = [
        (None, {'fields': ['name', 'price']}),
        (_('Option'), {'fields': ['enabled', 'categories']}),
    ]

detail = ItemDetail.as_view()


class ItemCreate(CreateAndDuplicateView):
    model = models.Item2
    form_class = forms.ItemForm
    success_url = reverse_lazy('sampleapp2:item2:list')
    inlines = [DocumentFileInlineEdit]
    fieldsets = [
        (None, {'fields': ['name', 'price']}),
        (_('Option'), {'fields': ['enabled', 'categories']}),
    ]

create = ItemCreate.as_view()

class CategoryViewSet(viewset.ModelViewSet):
    model = models.Category
    namespace_prefix = 'sampleapp2'
    search_fields = (
        ('name', types.TEXT_WILDCARD),
    )
    list_url = '/category/?name='  # 一覧画面のURLを指定する例

    def can_create(self, request):
        # kengen01の権限を持っている場合のみ作成を許可
        return role_api.request_has_permission(request, 'kengen01')

    def can_update(self, request):
        # kengen01の権限を持っている場合のみ編集を許可
        return role_api.request_has_permission(request, 'kengen01')

    def can_delete(self, request):
        # kengen01の権限を持っている場合のみ削除を許可
        return role_api.request_has_permission(request, 'kengen01')

category_viewset = CategoryViewSet()

class DocumentListView(ListView):
    model = models.DocumentFile
    default_search = True
    show_button_search = False

    show_button_download_csv = True
    show_button_download_excel = True

class DocumentFileViewSet(viewset.ModelViewSet):
    model = models.DocumentFile
    namespace_prefix = 'sampleapp2'
    list_view = DocumentListView

    def can_duplicate(self, request):
        """複製は動かないのでメニューを無効にしておく
        """
        return False

document_file_viewset = DocumentFileViewSet()

class DocumentFileDownloadFileView(files_views.DownloadFileView):
    model = models.DocumentFile

document_file_download_file_view = DocumentFileDownloadFileView.as_view()

# modelに定義されていない検索フィールド
SEARCH_CNT = {}
SEARCH_CNT.update(types.TEXT_EXACTRY)
SEARCH_CNT['modelfield'] = django_models.IntegerField(_("Count"))
SEARCH_CNT['field'] = django_forms.IntegerField

class EntryListSQL(SQLListView):
    """Entryモデルを日付で集約して表示するビュークラス
    """
    model = models.Entry
    query = """
        SELECT
          id,
          date,
          count(*) as cnt
        FROM sampleapp2_entry
        WHERE
          1 = 1
          {% if date.0 and not date.1 %}AND date >= #date[0]#{% endif %}
          {% if date.1 and not date.0 %}AND date < #date[1]#{% endif %}
        GROUP BY date
        {% if cnt %} HAVING cnt = #cnt# {% endif %}
        {{order_clause}}
    """
    list_display = [
        'date',
        'cnt'
    ]
    list_sortable = [
        'date',
        'cnt'
    ]
    default_order = ['date']
    column_names = [('cnt', _("Count"))]
    search_fields = {'date': types.DATERANGE,
                     'cnt': SEARCH_CNT}
    show_detail_menu = False
    show_button_create = False

entry_list_sql_view = EntryListSQL.as_view()

class TagListView(ListView):
    model = models.Tag
    search_fields = (
        ('name', types.TEXT_WILDCARD),
    )
    list_display = ('name', 'memo')
    fix_cols = 2

class TagViewSet(viewset.ModelViewSet):
    model = models.Tag
    namespace_prefix = 'sampleapp2'
    list_view = TagListView

tag_viewset = TagViewSet()
