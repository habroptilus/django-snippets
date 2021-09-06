from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from snippets.models import Snippet, Comment
from django.contrib.auth.decorators import login_required
from snippets.forms import SnippetForm, CommentForm

# Create your views here.


def top(request):
    """snippetの一覧を表示する"""
    snippets = Snippet.objects.all()
    context = {"snippets": snippets}  # htmlに渡すデータをdict形式で
    return render(request, "snippets/top.html", context)


@login_required  # ログインしないとできない処理
def snippet_new(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)  # request.POSTにフォームに入力されたパラメータが入っている
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            # snippet.idじゃだめ？
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:  # getのとき
        form = SnippetForm()

    return render(request, "snippets/snippet_new.html", {"form": form})


@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)  # pk=にしないとだめだった...
    if snippet.created_by != request.user:
        return HttpResponseForbidden("このスニペットの編集は許可されていません")
    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)  # 編集対象をinstanceに入れる
        if form.is_valid():
            snippet = form.save()
            return redirect("snippet_detail", snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, "snippets/snippet_edit.html", {"form": form})


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    comments = Comment.objects.filter(commented_to=snippet)
    return render(request, "snippets/snippet_detail.html", {'snippet': snippet, "comments": comments})


@login_required
def comment_new(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if request.method == "POST":
        form = CommentForm(request.POST)  # request.POSTにフォームに入力されたパラメータが入っている
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commented_by = request.user
            comment.commented_to = snippet
            comment.save()
            # snippet.idじゃだめ？
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:  # getのとき
        form = CommentForm()

    return render(request, "comments/comment_new.html", {"form": form})
