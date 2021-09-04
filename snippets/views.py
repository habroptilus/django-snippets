from django.http import HttpResponse
from django.shortcuts import render
from snippets.models import Snippet
# Create your views here.


def top(request):
    """snippetの一覧を表示する"""
    snippets = Snippet.objects.all()
    context = {"snippets": snippets}  # htmlに渡すデータをdict形式で
    return render(request, "snippets/top.html", context)


def snippet_new(request):
    return HttpResponse("スニペットの登録")


def snippet_edit(request):
    return HttpResponse("スニペットの編集")


def snippet_detail(request):
    return HttpResponse("スニペットの詳細閲覧")
