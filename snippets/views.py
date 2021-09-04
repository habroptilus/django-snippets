from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    return render(request, "snippets/snippet_detail.html", {'snippet': snippet})
