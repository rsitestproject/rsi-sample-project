# -*- coding: utf-8 -*-
from sample_project.settings import *


INSTALLED_APPS += (
    'rsi.azure',
    'sampleapp3',
)


######################
# 認証方式の設定
######################

AUTHENTICATION_BACKENDS = ('rsi.azure.auth.AzureAuthBackend',)
ROOT_URLCONF = 'sample_project.azure_urls'


######################
# メニューバーの設定
######################
MENUBAR_LEFT += ('sampleapp3.menu.SampleApp3Menu',)  # azure apiアクセステストページ

######################
# AzureAD認証の設定
######################

# azure
AZURE_AUTH_CLIENT_ID = '633d51ef-a772-4955-bb00-2c33d760461c'
AZURE_AUTH_CLIENT_SECRET = '+MBejkNHOGDeRaXddSF4CFZtFUUmUruBk3bo1+JEXCw='
AZURE_AUTH_TENANT_DOMAIN = 'chigira.onmicrosoft.com'
AZURE_AUTH_RESOURCE_URL = 'https://management.core.windows.net/'

######################
# Azure Storage の設定
######################

AZURE_STORAGE_ACCOUNT_NAME = 'beprouddevelop2'
AZURE_STORAGE_ACCOUNT_KEY = 'pHFBe0XYOxh0iubYjtGrmxJyJJXQt4o/uXZFCfQuP3dStBX8YFBDlAAsu08saZgh+vj6n2v/TmTwhTeQpgP//w=='
