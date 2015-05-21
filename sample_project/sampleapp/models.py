# coding: utf-8
import os
import time

from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


STATUS_CHOICES = (
    (1, 'Default'),
    (2, 'Success'),
    (3, 'Warning'),
    (4, 'Approved'),
    (5, '------'),
)

CATEGORY_CHOICES = (
    (1, 'OK'),
    (2, 'NG'),
)


@python_2_unicode_compatible
class Factory(models.Model):
    """製造場所
    """
    name = models.CharField(u"工場名", max_length=100)
    category = models.CharField(u"区分", max_length=100, null=True, blank=True)
    address = models.CharField(u"住所", max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = u'製造場所'


@python_2_unicode_compatible
class Material(models.Model):
    """材料マスタ
    """
    name = models.CharField(_('Name'), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = u'材料マスタ'


def file_filename(instance, filename):
    """ファイル名を生成する関数
    タイムスタンプ+元ファイルの拡張子のパスを返す
    """
    return str(int(time.time())) + os.path.splitext(filename)[1]


@python_2_unicode_compatible
class Item(models.Model):
    """品物
    """
    name = models.CharField(_('Name'), max_length=100)
    date = models.DateField(_('Date'), null=True, blank=True)
    status = models.IntegerField(
        _('Status'), choices=STATUS_CHOICES, null=True, blank=True)
    category = models.IntegerField(
        _('Category'), choices=CATEGORY_CHOICES, null=True, blank=True)
    enabled = models.BooleanField(
        _('Enabled/Disabled'), help_text=_('Check if enabled'))
    value = models.DecimalField(
        _('Number'), decimal_places=3, max_digits=10, null=True, blank=True)
    memo = models.TextField(_('Memo'), null=True, blank=True)
    factory = models.ForeignKey(
        Factory, verbose_name=_('Factory'), null=True, blank=True)
    file = models.FileField(
        upload_to=file_filename, verbose_name=_('File'), null=True, blank=True,
        help_text=_('Select a file to upload'))

    def get_enabled_display(self):
        if self.enabled in [True, 1, '1']:
            return u"有効"
        elif self.enabled in [False, 0, '0']:
            return u"無効"

    get_enabled_display.short_description = _('Enabled/Disabled')

    def get_value_display(self):
        if self.value is not None:
            return "{:,}".format(self.value)

    get_value_display.short_description = _('Number')
    get_value_display.align = "right"

    name.truncate_length = 40
    factory.detail_url = 'test'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

if six.PY2:
    Item.get_status_display.__func__.short_description = _('Status')
    Item.get_category_display.__func__.short_description = _('Category')
else:
    Item.get_status_display.short_description = _('Status')
    Item.get_category_display.short_description = _('Category')


class ItemMaterial(models.Model):
    """品物に紐付く材料
    """
    item = models.ForeignKey(Item, verbose_name=_('Item'))
    material = models.ForeignKey(Material, verbose_name=_('Material'))
    quantity = models.IntegerField(_('Quantity'))
    memo = models.TextField(_('Memo'), null=True, blank=True)
