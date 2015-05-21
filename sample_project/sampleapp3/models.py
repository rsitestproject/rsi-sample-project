# coding: utf-8
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from rsi.common import models as common_models
from rsi.azure import models as files_models


@python_2_unicode_compatible
class DocumentFile2(files_models.AbstractFile,
                    common_models.RsiCommonInfo, models.Model):
    """Azure 文書ファイル
    """
    description = models.CharField(
        _('Description'), max_length=20, blank=True, null=True)

    container = 'documentfile2'

    def __str__(self):
        return u"{}".format(self.name)

    __str__.short_description = _('Azure Document file')

    class Meta:
        verbose_name = _('Azure Document file')
        verbose_name_plural = _('Azure Document files')

    def get_download_url(self):
        """ダウンロードURLを返します
        """
        return reverse(
            'sampleapp3:document_file_download', kwargs={'pk': self.pk})
