from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import resolve
from snippets.views import snippet_new, snippet_edit, snippet_detail

from snippets.models import Snippet
from snippets.views import top

UserModel = get_user_model()


class TopPageTest(TestCase):
    """ルーティング(urlとビュー関数を結びつける)とその中身のテスト"""

    def test_top_page_returns_200_and_expected_title(self):
        """200番がかえってきていること、指定した文字列が含まれていることを確認する"""
        response = self.client.get(
            "/")  # self.clientはDjangoのTestCaseが事前に読み込んでくれている
        self.assertContains(response, "Djangoスニペット", status_code=200)

    def test_top_page_users_expected_template(self):
        """指定したtemplateを使用しているかを確認する"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "snippets/top.html")


class TopPageRenderSnippetsTest(TestCase):
    def setUp(self):
        # テストケースの終わりにこれらのレコードはロールバックされる
        # setupとかtypoすると自動でテスト前に動いてくれない.正しくsetUpというメソッド名を指定する必要がある
        self.user = UserModel.objects.create(
            username="test_user1",
            email="test@example.com",
            password="passpass1234"
        )
        self.snippet = Snippet.objects.create(
            title="test_title",
            code="print('hello')",
            description="description111",
            created_by=self.user
        )

    def test_should_return_snippet_title(self):
        """userを指定してtopページにリクエストしたらスニペットのtitleが表示されていること"""
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.snippet.title)

    def test_should_return_username(self):
        """usernameがresponseに含まれていること"""
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)


class CreateSnippetTest(TestCase):
    def test_should_resolve_snippet_new(self):
        found = resolve("/snippets/new/")  # こっちは先頭のスラッシュを省略しない
        self.assertEqual(snippet_new, found.func)


class SnippetDetailTest(TestCase):
    def test_should_resolve_snippet_detail(self):
        found = resolve("/snippets/1/")  # こっちは先頭のスラッシュを省略しない
        self.assertEqual(snippet_detail, found.func)


class EditSnippetTest(TestCase):
    def test_should_resolve_snippet_edit(self):
        found = resolve("/snippets/1/edit/")  # こっちは先頭のスラッシュを省略しない
        self.assertEqual(snippet_edit, found.func)
