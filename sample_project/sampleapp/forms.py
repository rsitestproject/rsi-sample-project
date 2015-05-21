# coding: utf-8
from django import forms

from rsi.common.forms import fields
from rsi.common.forms import widgets
from rsi.common.forms import models as forms_models

from . import models

STATUS_CHOICES = (
    ('', '--------'),
) + models.STATUS_CHOICES
CATEGORY_CHOICES = models.CATEGORY_CHOICES


class SearchForm(forms.Form):
    """検索フォーム
    """
    name = fields.CharField(required=False, label=u"品名")
    date_range = fields.DateRangeField(required=False, label=u"日付")
    status = forms.ChoiceField(
        required=False, choices=STATUS_CHOICES, label=u"状態")
    category = forms.ChoiceField(
        required=False, choices=CATEGORY_CHOICES,
        widget=widgets.RadioSelect(inline=True), label=u"区分")
    enabled = forms.BooleanField(required=False, label=u"有効のみ表示")
    # TODO:製造場所


class ItemForm(forms_models.ModelForm):
    """Item追加フォーム
    """
    class Meta:
        model = models.Item
        fields = (
            'name', 'date', 'status', 'category', 'enabled', 'value', 'memo',
            'file')
        widgets = {
            'memo': widgets.Textarea(attrs={'maxlength': 100, 'cols': 120, 'rows': 5}),
            'date': widgets.DateInput,
            'name': widgets.TextInput(attrs={'readonly':"readonly"}),
        }
