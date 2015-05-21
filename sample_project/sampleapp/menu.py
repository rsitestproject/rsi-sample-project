# coding: utf-8
from django.core.urlresolvers import reverse_lazy

from rsi.menubar import menu


class ListMenu(menu.Menu):
    label = u"一覧画面"
    default_subitems = [
        'sampleapp.menu.ListMenuItem',
        'sampleapp.menu.ListHeaderMenuItem',
        'sampleapp.menu.ListColMenuItem',
        'sampleapp.menu.ListColHeadMenuItem',
        'sampleapp.menu.ListSQLMenuItem',
    ]


class ListMenuItem(menu.MenuItem):
    label = u"ページャ付"
    url = reverse_lazy('sampleapp:item:list')


class ListHeaderMenuItem(menu.MenuItem):
    label = u"ヘッダ固定"
    url = reverse_lazy('sampleapp:list_header')


class ListColMenuItem(menu.MenuItem):
    label = u"カラム固定"
    url = reverse_lazy('sampleapp:list_col')


class ListColHeadMenuItem(menu.MenuItem):
    label = u"ヘッダカラム固定"
    url = reverse_lazy('sampleapp:list_col_head')


class ListSQLMenuItem(menu.MenuItem):
    label = u"SQL直接指定"
    url = reverse_lazy('sampleapp:list_sql')


class DetailMenu(menu.Menu):
    label = u"詳細画面"
    default_subitems = [
        'sampleapp.menu.DetailNormalMenuItem',
        'sampleapp.menu.DetailAddTabMenuItem',
        'sampleapp.menu.DetailAddAccordionMenuItem',
        'rsi.menubar.menu.Separator',
        'sampleapp.menu.DetailTabMenuItem',
        'sampleapp.menu.DetailAccordionMenuItem',
    ]


class DetailNormalMenuItem(menu.MenuItem):
    label = u"登録モード(通常版)"
    url = reverse_lazy('sampleapp:item:create')


class DetailAddTabMenuItem(menu.MenuItem):
    label = u"登録モード(タブ版)"
    url = reverse_lazy('sampleapp:add_tab')


class DetailAddAccordionMenuItem(menu.MenuItem):
    label = u"登録モード(アコーディオン版)"
    url = reverse_lazy('sampleapp:add_accordion')


class DetailTabMenuItem(menu.MenuItem):
    label = u"照会モード(タブ版)"
    url = reverse_lazy('sampleapp:detail_tab', kwargs={'pk': '1'})


class DetailAccordionMenuItem(menu.MenuItem):
    label = u"照会モード(アコーディオン版)"
    url = reverse_lazy('sampleapp:detail_accordion', kwargs={'pk': '1'})


class OtherMenu(menu.Menu):
    label = u"その他"
    default_subitems = [
        'sampleapp.menu.OtherUploadMenuItem',
        'sampleapp.menu.OtherHistoryMenuItem',
        'rsi.menubar.menu.Separator',
        'sampleapp.menu.OtherBaseTemplateMenuItem',
        'rsi.menubar.menu.Separator',
        'sampleapp.menu.OtherSubMenu',
    ]


class OtherUploadMenuItem(menu.MenuItem):
    label = u"アップロード画面"
    url = reverse_lazy('sampleapp:upload')


class OtherHistoryMenuItem(menu.MenuItem):
    label = u"変更履歴画面"


class OtherBaseTemplateMenuItem(menu.MenuItem):
    label = u"ベーステンプレート"
    url = reverse_lazy('sampleapp:base_template')


class OtherSubMenuItem1(menu.MenuItem):
    label = u"サブメニュー項目1"


class OtherSubMenuItem2(menu.MenuItem):
    label = u"サブメニュー項目2"


class OtherSubMenu(menu.SubMenu):
    label = u"サブメニュー"
    default_subitems = [
        'sampleapp.menu.OtherSubMenuItem1',
        'sampleapp.menu.OtherSubMenuItem2',
    ]


class PermissionMenu(menu.Menu):
    label = u"権限"
    default_subitems = [
        'sampleapp.menu.PermissionMenuItem1',
        'sampleapp.menu.PermissionMenuItem2',
        'sampleapp.menu.PermissionMenuItem3',
        'rsi.menubar.menu.Separator',
        'sampleapp.menu.PermissionFilter',
    ]


class PermissionMenuItem1(menu.MenuItem):
    label = u"権限が不要な項目"


class PermissionMenuItem2(menu.MenuItem):
    label = u"権限「kengen01」が必要な項目"
    url = reverse_lazy('sampleapp:permission_01')
    require_permissions = ['kengen01']


class PermissionMenuItem3(menu.MenuItem):
    label = u"権限「kengen02」が必要な項目"
    url = reverse_lazy('sampleapp:permission_02')
    require_permissions = ['kengen02']


class PermissionFilter(menu.MenuItem):
    label = u"テンプレートフィルタで権限チェック"
    url = reverse_lazy('sampleapp:permission_filter')
