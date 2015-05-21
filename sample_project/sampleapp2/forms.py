# coding: utf-8
from rsi.common.forms.models import ModelForm
from rsi.common.forms import widgets

from . import models


class ItemForm(ModelForm):
    class Meta:
        model = models.Item2
        widgets = {
            'enabled': widgets.RadioSelectBoolean,
            'categories': widgets.CheckboxSelectMultiple,
        }
