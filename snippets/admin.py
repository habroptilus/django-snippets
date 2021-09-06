from django.contrib import admin
from snippets.models import Snippet, Comment
# Register your models here.

# 管理画面で利用するためにSnippetクラスを追加
# これでSnippetテーブルを管理画面からいじることができる

admin.site.register(Snippet)
admin.site.register(Comment)
