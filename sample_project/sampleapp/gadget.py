# coding: utf-8
from django.core.urlresolvers import reverse

from rsi.gadgets.todo_list import todo
from rsi.gadgets.todo_list import gadget

from . import models


class SampleAppTODOListGadget(gadget.TODOListGadget):
    """TODOリストの実装
    """
    default_items = (
        'sampleapp.gadget.EnabledTODOItem',
        'sampleapp.gadget.SuccessStatusTODOItem',
    )


class EnabledTODOItem(todo.TODOItem):
    """有効なTODO項目
    """
    label = u"有効な品物"
    queryset = models.Item.objects.filter(enabled=1)

    def get_link(self):
        return reverse('sampleapp:list_col') + '?enabled=on'


class SuccessStatusTODOItem(todo.TODOItem):
    """状態=SuccessなTODO項目
    """
    label = u"状態=Successなデータ"
    queryset = models.Item.objects.filter(status=2)

    def get_link(self):
        return reverse('sampleapp:list_col') + '?status=2'
