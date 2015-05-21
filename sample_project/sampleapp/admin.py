# coding: utf-8
from django.contrib import admin

from . import models


admin.site.register(models.Material)


class ItemMaterialInline(admin.TabularInline):
    model = models.ItemMaterial
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemMaterialInline]

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Factory)
