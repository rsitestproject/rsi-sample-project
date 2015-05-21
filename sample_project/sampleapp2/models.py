# coding: utf-8
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.urlresolvers import reverse

from rsi.common import models as common_models
from rsi.common.files import models as files_models

PRICE_CHOICES = (
    (0, u'0円'),
    (100, u'100円'),
    (500, u'500円'),
    (1000, u'1000円'),
    (5000, u'5000円'),
    (10000, u'10000円'),
)


@python_2_unicode_compatible
class Category(common_models.RsiCommonInfo):
    """カテゴリ
    """
    name = models.CharField(_('Name'), max_length=30)

    def __str__(self):
        return u"{}".format(self.name)

    __str__.short_description = _('Category')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


@python_2_unicode_compatible
class Item2(common_models.RsiCommonInfo):
    """商品
    """
    name = models.CharField(_('Name'), max_length=30)
    price = models.PositiveIntegerField(
        _('Price'), choices=PRICE_CHOICES, null=False, default=0)
    enabled = models.BooleanField(_('Enabled/Disabled'), default=True)
    categories = models.ManyToManyField('Category', blank=True, verbose_name=_('Categories'))

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')


@python_2_unicode_compatible
class DocumentFile(files_models.AbstractFile, common_models.RsiCommonInfo, models.Model):
    """文書ファイル
    """
    description = models.CharField(_('Description'), max_length=20, blank=True, null=True)
    item = models.ForeignKey(Item2, verbose_name=_('Item'), blank=True, null=True)

    def __str__(self):
        return u"{}".format(self.name)

    __str__.short_description = _('Document file')

    class Meta:
        verbose_name = _('Document file')
        verbose_name_plural = _('Document files')

    def get_download_url(self):
        """ダウンロードURLを返します
        """
        return reverse('sampleapp2:document_file_download', kwargs={'pk': self.pk})


@python_2_unicode_compatible
class Entry(common_models.RsiCommonInfo):
    """エントリ
    """
    title = models.CharField(_('Title'), max_length=20)
    body = models.TextField(_('Body'))
    date = models.DateField(_('Date'), default=timezone.now)

    def __str__(self):
        return u"{}".format(self.title)

    __str__.short_description = _('Entry')

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        db_table = 'sampleapp2_entry'


@python_2_unicode_compatible
class Tag(common_models.RsiCommonInfo):
    """タグ
    """
    name = models.CharField(_('Name'), max_length=20, primary_key=True)
    memo = models.TextField(_('Memo'), null=True, blank=True)

    def __str__(self):
        return u"{}".format(self.name)

    __str__.short_description = _('Name')

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tag')
