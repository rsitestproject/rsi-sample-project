# coding: utf-8
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _

from rsi.menubar import menu


class SampleApp2Menu(menu.Menu):
    label = u"sampleapp2"
    default_subitems = [
        'sampleapp2.menu.Item2ListMenuItem',
        'sampleapp2.menu.Item2ListSidebarMenuItem',
        'sampleapp2.menu.CategoryListMenuItem',
        'sampleapp2.menu.DocumentFileListMenuItem',
        'sampleapp2.menu.EntryListSQLMenuItem',
        'sampleapp2.menu.TagMenuItem',
    ]


class Item2ListMenuItem(menu.MenuItem):
    label = _("Item")
    url = reverse_lazy('sampleapp2:item2:list')


class Item2ListSidebarMenuItem(menu.MenuItem):
    label = _("Item(Sidebar)")
    url = reverse_lazy('sampleapp2:item2:list_sidebar')


class CategoryListMenuItem(menu.MenuItem):
    label = _("Category")

    def get_url(self):
        return reverse('sampleapp2:category:list') + '?name='


class DocumentFileListMenuItem(menu.MenuItem):
    label = _("Document file")
    url = reverse_lazy('sampleapp2:documentfile:list')


class EntryListSQLMenuItem(menu.MenuItem):
    label = _("Entries(SQL)")
    url = reverse_lazy('sampleapp2:entry_list_sql')


class TagMenuItem(menu.MenuItem):
    label = _("Tag")
    url = reverse_lazy('sampleapp2:tag:list')
