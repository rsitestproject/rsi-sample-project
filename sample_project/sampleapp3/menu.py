# coding: utf-8
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from rsi.menubar import menu


class SampleApp3Menu(menu.Menu):
    label = u"sampleapp3"
    default_subitems = [
        'sampleapp3.menu.DocumentFileListMenuItem',
        'sampleapp3.menu.AADUserListMenuItem',
    ]


class DocumentFileListMenuItem(menu.MenuItem):
    label = _("Azure Document file")
    url = reverse_lazy('sampleapp3:documentfile2:list')


class AADUserListMenuItem(menu.MenuItem):
    label = _("Graph API")
    url = reverse_lazy('sampleapp3:aad_userlist')
