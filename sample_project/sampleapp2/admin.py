# coding: utf-8
from django.contrib import admin

from rsi.common import admin_helper

from . import models


admin.site.register(models.Category, admin_helper.ModelAdmin)
admin.site.register(models.Item2, admin_helper.ModelAdmin)
admin.site.register(models.Entry, admin_helper.ModelAdmin)
admin.site.register(models.Tag, admin_helper.ModelAdmin)
