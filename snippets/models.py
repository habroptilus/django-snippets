from django.db import models
from django.conf import settings

# Create your models here.


class Snippet(models.Model):
    title = models.CharField("タイトル", max_length=128)
    code = models.TextField("コード", blank=True)
    description = models.TextField("説明", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE)  # userが削除されたら紐づくsnippetも削除

    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField("コメント本文", blank=False)
    commented_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="コメント投稿者", on_delete=models.CASCADE)
    commented_to = models.ForeignKey(
        Snippet, verbose_name="コメント先のスニペット", on_delete=models.CASCADE
    )
    commented_at = models.DateTimeField("コメント投稿日", auto_now_add=True)

    def __str__(self):
        return self.text
