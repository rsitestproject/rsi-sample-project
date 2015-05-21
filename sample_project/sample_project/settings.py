# coding: utf-8
"""
Django settings for sample_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p^fani8errgq*^735wetcn4xfe)i0cq#j7)fqfvvfboc0+ylf-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django_extensions',
    # 'debug_toolbar',
    'rsi.base',
    'rsi.common',
    'rsi.menubar',
    'rsi.uniquepost',
    'rsi.role',
    'rsi.auth_ext',
    'rsi.dashboard',
    'rsi.blobstorage',
    'rsi.gadgets.image_display',
    'rsi.gadgets.information',
    'rsi.gadgets.links',
    'rsi.gadgets.todo_list',
    'sampleapp',
    'sampleapp2',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 言語切替
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'rsi.uniquepost.middleware.UniquePostMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rsi.auth_ext.middleware.PositionMiddleware',  # 兼務設定
)

ROOT_URLCONF = 'sample_project.urls'

WSGI_APPLICATION = 'sample_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# アップロードしたファイル
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# テンプレートファイルを読み込むディレクトリ
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# 多言語設定
from django.utils.translation import ugettext_lazy
LANGUAGES = (
    ('ja', ugettext_lazy('Japanese')),
    ('en', ugettext_lazy('English')),
    ('zh', ugettext_lazy('Chinese')),
)

# コンテキストプロセッサ
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'rsi.common.context_processors.common_context',
    'rsi.auth_ext.context_processors.auth_config',
)

# デフォルト設定の読み込み
from rsi.conf.default_settings import *  # NOQA

# 認証ページの設定
USE_I18N_LOGIN_FORM = True

# commonの設定
COMMON_SHOW_FOOTER = True

########################
# ダッシュボードの設定
########################
# 左のガジェット
GADGET_LEFT = (
    'rsi.gadgets.image_display.gadget.ImageDisplayGadget',
)
# 中央のガジェット
GADGET_CENTER = (
    'rsi.gadgets.information.gadget.InformationGadget',
)
# 右のガジェット
GADGET_RIGHT = (
    'sampleapp.gadget.SampleAppTODOListGadget',
    'rsi.gadgets.links.gadget.LinksGadget',
)

######################
# メニューバーの設定
######################
MENUBAR_LEFT = (
    'sampleapp.menu.ListMenu',  # 一覧画面
    'sampleapp.menu.DetailMenu',  # 詳細画面
    'sampleapp.menu.OtherMenu',  # その他
    'sampleapp.menu.PermissionMenu',  # 権限
    'sampleapp2.menu.SampleApp2Menu',  # サンプルアプリその2
)
SHOW_SELECT_LANGUAGE_MENU = True  # 言語選択メニューの表示
