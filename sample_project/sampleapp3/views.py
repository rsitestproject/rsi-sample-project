# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rsi.azure import auth as azure_auth
from rsi.common.files import views as files_views
from rsi.common.views import viewset
from rsi.common.views.list import ListView

from . import models


class DocumentListView(ListView):
    model = models.DocumentFile2
    default_search = True
    show_button_search = False


class DocumentFileViewSet(viewset.ModelViewSet):
    model = models.DocumentFile2
    namespace_prefix = 'sampleapp3'
    list_view = DocumentListView

    def can_duplicate(self, request):
        """複製は動かないのでメニューを無効にしておく
        """
        return False

document_file_viewset = DocumentFileViewSet()


class DocumentFileDownloadFileView(files_views.DownloadFileView):
    model = models.DocumentFile2

document_file_download_file_view = DocumentFileDownloadFileView.as_view()


@login_required
def aad_userlist(request):
    """Azure APIへのアクセステスト"""

    session = azure_auth.get_oauth_session(request)
    response = session.get('https://graph.windows.net/725860ce-8aa7-4684-8e25-c671663da617/users?api-version=2013-04-05')  # NOQA
    users = response.json()['value']
    return render(request, 'sampleapp3/aad_userlist.html', {'users': users})
