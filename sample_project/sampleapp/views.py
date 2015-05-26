# coding: utf-8
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.db import models as django_models
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from rsi.uniquepost.decorators import unique_post
from rsi.common.views.list import ListView, SQLListView
from rsi.common.views.edit import (
    CreateAndDuplicateView, InlineEdit, UpdateView, DeleteView)
from rsi.common.views.detail import DetailView
from rsi.common.views import viewset
from rsi.common.views import upload
from rsi.common.views import download
from rsi.common.search import types
from rsi.common import dataset
from rsi.role.decorators import require_permissions

from . import models
from . import forms

LIST_DISPLAY = [
    'name',
    'date',
    'get_status_display',
    'get_category_display',
    'get_enabled_display',
    'get_value_display',
    'factory',
    'memo',
]
LIST_SORTABLE = [
    'name',
    ('get_status_display', 'status'),
    ('get_category_display', 'category'),
    ('get_enabled_display', 'enabled'),
    ('get_value_display', 'value'),
    'factory',
    'memo',
]


class List(ListView):
    """ページャ付
    """
    model = models.Item
    paginate_by = 3
    list_display = LIST_DISPLAY
    list_sortable = LIST_SORTABLE
    show_number = True
    page_description = u"ページャ版"
    search_fields = (
        ('name', types.TEXT_WILDCARD),
        ('factory', types.FK_SELECT_MULTIPLE),
        ('status', types.SELECT_DROPDOWN),
        ('category', types.SELECT_RADIO),
        ('date', types.DATERANGE),
        ('enabled', types.CHECKBOX),
    )

    show_button_download_csv = True
    show_button_download_excel = True


class ListDownload(download.DownloadMixin, List):
    # アップロード可能なデータを生成するために、
    # フィールド名の指定を変える。
    list_display = [
        'name',
        'date',
        'get_status_display',
        'get_category_display',
        'get_enabled_display',
        'get_value_display',
        'factory',
        'memo',
    ]


class ListHeader(ListView):
    """ヘッダ固定
    """
    model = models.Item
    list_display = LIST_DISPLAY
    list_sortable = LIST_SORTABLE
    default_order = []
    show_number = True
    fix_height = 500
    page_description = u"ヘッダ固定版"
    search_fields = (
        ('name', types.TEXT_CONTAINS),
        ('factory', types.FK_CHECKBOX_MULTIPLE),
        ('status', types.SELECT_DROPDOWN),
        ('category', types.CHECKBOX_MULTIPLE),
        ('date', types.DATERANGE),
        ('enabled', types.CHECKBOX),
    )

list_header = ListHeader.as_view()


class ListCol(ListView):
    """カラム固定
    """
    model = models.Item
    list_display = LIST_DISPLAY
    list_sortable = LIST_SORTABLE
    show_number = True
    fix_cols = 3
    page_description = u"カラム固定版"
    multi_select = True
    search_fields = (
        ('name', types.TEXT_MULTIPLE),
        ('factory', types.FK_CHECKBOX_MULTIPLE),
        ('status', types.SELECT_MULTIPLE),
        ('category', types.SELECT_RADIO),
        ('date', types.DATE),
        ('enabled', types.CHECKBOX),
    )

list_col = ListCol.as_view()


class ListColHead(ListView):
    """ヘッダカラム固定
    """
    model = models.Item
    list_display = LIST_DISPLAY
    list_sortable = LIST_SORTABLE
    fix_cols = 3
    fix_height = 150
    page_description = u"ヘッダカラム固定版"
    search_type = 'sidebar'
    search_sidebar = {
        'filter': [
            'factory',
            'status',
            'category',
        ],
        'freetext': [
            'name',
        ],
    }

list_col_head = ListColHead.as_view()



SEARCH_SUMVAL = {'modelfield': django_models.IntegerField(u"合計値")}
SEARCH_SUMVAL.update(types.TEXT_EXACTRY)

class ListSQL(SQLListView):
    """SQLベース
    """
    model = models.Item
    paginate_by = 3
    query = """
        SELECT 
          id,
          name,
          date,
          sum(value) as sumval
        FROM
          sampleapp_item
        WHERE 1=1
          {% if name %}AND name=#name#{% endif %}
          {% if enabled %}AND enabled=#enabled#{% endif %}
          {% if factory %}AND factory_id=#factory#{% endif %}
          {% if date.0 and date.1 %}AND date BETWEEN #date[0]# and #date[1]#{% endif %}
          {% if date.0 and not date.1 %}AND date >= #date[0]#{% endif %}
          {% if date.1 and not date.0 %}AND date < #date[1]#{% endif %}
          {% if status %}AND status in #status#{% endif %}
        GROUP BY
          name
        HAVING 1=1
          {% if sumval %}AND sumval=#sumval#{% endif %}
        {{order_clause}}
        {{limit_clause}}
    """
    list_display = [
        'name',
        'date',
        'get_status_display',
        'get_category_display',
        'get_enabled_display',
        'sumval',
        'factory',
        'memo',
    ]
    list_sortable = [
        'name',
        'sumval',
        ('get_status_display', 'status'),
    ]
    column_names = [('sumval', u"value合計値")]
    show_number = True
    page_description = u"SQL版"
    search_fields = {
        'name': types.TEXT_EXACTRY,
        'sumval': SEARCH_SUMVAL,
        'enabled': types.CHECKBOX,
        'date': types.DATERANGE,
        'status': types.SELECT_MULTIPLE,
        'factory': types.SELECT_DROPDOWN,
    }

list_sql = ListSQL.as_view()


class ItemMaterialInlineEdit(InlineEdit):
    label = u"材料"
    model = models.ItemMaterial
    override_params = {
        'extra': 2,
        'widgets': {
            'memo': django_forms.Textarea(attrs={'cols': 120, 'rows': 3}),
        },
    }


class CorrelationCheck(object):
    """相関チェック
    """
    def clean_material_quantity(self, form, inlines):
        """状態がDefaultの場合は材料は最低2個以上
        """
        if not inlines:
            return
        if form.cleaned_data['status'] != 1:
            return
        material_quantity = 0
        for formset in inlines:
            for inline_form in formset:
                material_quantity += int(inline_form.cleaned_data.get('quantity') or 0)
        if material_quantity < 2:
            raise ValidationError(u'状態がDefaultの場合、材料は最低2個以上指定してください')


class ItemAdd(CorrelationCheck, CreateAndDuplicateView):
    """詳細画面通常版
    """
    clean_methods = [
        'clean_material_quantity',
    ]
    model = models.Item
    form_class = forms.ItemForm
    success_url = reverse_lazy('sampleapp:item:list')
    inlines = [ItemMaterialInlineEdit]
    fieldsets = (
        (None, {
            'fields': ['name', 'date', 'status', 'category', 'enabled', 'value', 'file']}),
        (_('Memo'), {'fields': ['memo']}),
    )


class ItemEdit(CorrelationCheck, UpdateView):
    """詳細画面通常版
    """
    clean_methods = [
        'clean_material_quantity',
    ]
    model = models.Item
    form_class = forms.ItemForm
    success_url = reverse_lazy('sampleapp:item:list')
    inlines = [ItemMaterialInlineEdit]
    fieldsets = (
        (None, {
            'fields': ['name', 'date', 'status', 'category', 'enabled', 'value', 'file']}),
        (_('Memo'), {'fields': ['memo']}),
    )


class ItemAddTab(CreateAndDuplicateView):
    """詳細画面タブ版
    """
    model = models.Item
    form_class = forms.ItemForm
    success_url = reverse_lazy('sampleapp:item:list')
    fieldset_display_style = 'tab'
    inlines = [ItemMaterialInlineEdit]
    fieldsets = (
        (None, {
            'fields': ['name', 'date', 'status', 'category', 'enabled', 'value', 'file']}),
        (_('Memo'), {'fields': ['memo']}),
    )

item_add_tab = unique_post(ItemAddTab.as_view())


class ItemAddAccordion(CreateAndDuplicateView):
    """詳細画面アコーディオン版
    """
    model = models.Item
    form_class = forms.ItemForm
    success_url = reverse_lazy('sampleapp:item:list')
    fieldset_display_style = 'accordion'
    inlines = [ItemMaterialInlineEdit]
    fieldsets = (
        (None, {
            'fields': ['name', 'date', 'status', 'category', 'enabled', 'value', 'file']}),
        (_('Memo'), {'fields': ['memo']}),
    )

item_add_accordion = unique_post(ItemAddAccordion.as_view())


class ItemDelete(DeleteView):
    """削除
    """
    model = models.Item
    success_url = reverse_lazy('sampleapp:item:list')


def base_template(request):
    """ベーステンプレート
    """
    messages.info(request, u'infoメッセージ')
    messages.success(request, u'successメッセージ')
    messages.warning(request, u'warningメッセージ')
    messages.error(request, u'errorメッセージ')
    return render(request, template_name='base/main.html')


class ItemDetail(DetailView):
    """照会
    """
    model = models.Item
    inlines = [ItemMaterialInlineEdit]


class ItemViewSet(viewset.ModelViewSet):
    """Itemモデルに対するViewSet
    """
    model = models.Item
    list_view = List
    create_view = ItemAdd
    update_view = ItemEdit
    delete_view = ItemDelete
    detail_view = ItemDetail
    download_view = ListDownload
    namespace_prefix = 'sampleapp'
    view_decorators = [
        unique_post,
    ]

item_view_set = ItemViewSet()


class ItemDetailTab(DetailView):
    """詳細画面タブ版
    """
    model = models.Item
    fieldset_display_style = 'tab'
    inlines = [ItemMaterialInlineEdit]
    fieldsets = (
        (None, {
            'fields': ['name', 'date', 'status', 'category', 'enabled', 'value', 'file']}),
        (_('Memo'), {'fields': ['memo']}),
    )

item_detail_tab = ItemDetailTab.as_view()


class ItemDetailAccordion(DetailView):
    """詳細画面タブ版
    """
    model = models.Item
    fieldset_display_style = 'accordion'
    inlines = [ItemMaterialInlineEdit]
    fieldsets = (
        (None, {
            'fields': ['name', 'date', 'status', 'category', 'enabled', 'value', 'file']}),
        (_('Memo'), {'fields': ['memo']}),
    )

item_detail_accordion = ItemDetailAccordion.as_view()


class ItemAddAccordion(CreateAndDuplicateView):
    """詳細画面アコーディオン版
    """
    model = models.Item
    form_class = forms.ItemForm
    success_url = reverse_lazy('sampleapp:item:list')
    fieldset_display_style = 'accordion'
    inlines = [ItemMaterialInlineEdit]
    fieldsets = (
        (None, {
            'fields': ['name', 'date', 'status', 'category', 'enabled', 'value', 'file']}),
        (_('Memo'), {'fields': ['memo']}),
    )

item_add_accordion = unique_post(ItemAddAccordion.as_view())


@require_permissions(['kengen01'])
def permission_01(request):
    """kengen01が必要なページ
    """
    messages.success(request, u'「kengen01」が必要なページです。')
    return render(request, template_name='base/main.html')


@require_permissions(['kengen02'])
def permission_02(request):
    """kengen02が必要なページ
    """
    messages.success(request, u'「kengen02」が必要なページです。')
    return render(request, template_name='base/main.html')


class ItemDeserializer(dataset.Deserializer):
    """CSV/Excelからの入力データをモデルに変換するクラス
    """
    model = models.Item
    fields = (
        (1, 'name'),
        (2, 'date'),
        (3, 'status', 'get_status_display'),
        (4, 'category', 'get_category_display'),
        (5, 'enabled', 'get_enabled_display'),
        (6, 'value'),
    )


class ItemUpload(upload.UploadView):
    """アップロード機能
    """
    model = models.Item
    deserializer = ItemDeserializer
    max_rows = 1000
    success_url = reverse_lazy('sampleapp:item:list')

item_upload = ItemUpload.as_view()
