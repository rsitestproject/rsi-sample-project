# coding: utf-8
from django.core.management.base import BaseCommand

from sampleapp2.models import Category

class Command(BaseCommand):
    help = u"排他制御を使う例"

    def handle(self, *args, **options):
        print u"排他制御を使う例"
        category = Category(name=u'排他制御を使う例')
        category.save()
        # 同じID(pk)のCategoryモデルのインスタンスを2つ取得(2箇所で取得)
        category1 = Category.objects.get(pk=category.pk)
        category2 = Category.objects.get(pk=category.pk)
        # 片方を変更して保存
        category1.name = 'update by category1'
        category1.save_exclusive()  # 排他制御を使う
        print "category1 saved."
        # もう片方を変更して保存
        category2.name = 'update by category2'
        category2.save_exclusive()  # 排他制御を使う(ここはエラーになる)
        print "category2 saved."
