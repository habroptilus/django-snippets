from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from snippets.models import Snippet, Comment
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
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user1",
            email="test@example.com",
            password="passpass1234"
        )
        self.client.force_login(self.user)  # ユーザーログイン

    def test_render_creation_form(self):
        """getで呼ばれたときにフォームを表示する."""
        response = self.client.get("/snippets/new/")  # 末尾のスラッシュを忘れない
        self.assertContains(response, "スニペットの登録", status_code=200)

    def test_create_snippet(self):
        data = {"title": "タイトル", "code": "コード", "description": "解説"}
        self.client.post("/snippets/new/", data)
        snippet = Snippet.objects.get(title="タイトル")
        self.assertEqual("コード", snippet.code)  # これ引数の順番大事？
        self.assertEqual("解説", snippet.description)


class SnippetDetailTest(TestCase):
    def setUp(self):
        # テストケースの終わりにこれらのレコードはロールバックされる
        # setupとかtypoすると自動でテスト前に動いてくれない.正しくsetUpというメソッド名を指定する必要がある
        self.user = UserModel.objects.create(
            username="test_user1",
            email="test@example.com",
            password="passpass5678"
        )
        self.snippet = Snippet.objects.create(
            title="test_title222",
            code="print('hello222')",
            description="description222",
            created_by=self.user
        )
        self.comment = Comment.objects.create(
            text="comment1",
            commented_by=self.user,
            commented_to=self.snippet
        )

    def test_should_use_expected_template(self):
        response = self.client.get(
            f"/snippets/{self.snippet.id}/")  # 末尾のスラッシュ忘れがち
        self.assertTemplateUsed(response, "snippets/snippet_detail.html")

    def test_detail_page_returns_200_and_expected_head(self):
        response = self.client.get(f"/snippets/{self.snippet.id}/")
        self.assertContains(response, self.snippet.title, status_code=200)

    def test_detail_page_returns_200_and_expected_comment(self):
        """snippetに紐づいたコメントが含まれていることを確認する."""
        response = self.client.get(f"/snippets/{self.snippet.id}/")
        self.assertContains(response, self.comment.text, status_code=200)


class EditSnippetTest(TestCase):
    def setUp(self):
        # テストケースの終わりにこれらのレコードはロールバックされる
        # setupとかtypoすると自動でテスト前に動いてくれない.正しくsetUpというメソッド名を指定する必要がある
        self.user = UserModel.objects.create(
            username="test_user1",
            email="test@example.com",
            password="passpass5678"
        )
        self.snippet = Snippet.objects.create(
            title="test_title222",
            code="print('hello222')",
            description="description222",
            created_by=self.user
        )

        self.client.force_login(self.user)

    def test_render_edit_form(self):
        """getで呼ばれたときに編集フォームを表示する."""
        response = self.client.get(
            f"/snippets/{self.snippet.id}/edit/")  # 末尾のスラッシュを忘れない
        self.assertContains(response, "スニペットの編集", status_code=200)

    def test_edit_snippet(self):
        data = {"title": "タイトルかえてやるぜ",
                "code": "コードかえてやるぜ"}
        self.client.post(f"/snippets/{self.snippet.id}/edit/", data)
        snippet = Snippet.objects.get(id=self.snippet.id)
        self.assertEqual("タイトルかえてやるぜ", snippet.title)
        self.assertEqual("コードかえてやるぜ", snippet.code)


class CreateCommentTest(TestCase):
    def setUp(self):
        # テストケースの終わりにこれらのレコードはロールバックされる
        # setupとかtypoすると自動でテスト前に動いてくれない.正しくsetUpというメソッド名を指定する必要がある
        self.user = UserModel.objects.create(
            username="test_user1",
            email="test@example.com",
            password="passpass5678"
        )
        self.snippet = Snippet.objects.create(
            title="test_title222",
            code="print('hello222')",
            description="description222",
            created_by=self.user
        )
        self.client.force_login(self.user)

    def test_render_creation_form(self):
        """getで呼ばれたときにフォームを表示する."""
        response = self.client.get(
            f"/snippets/{self.snippet.id}/comments/new/")  # 末尾のスラッシュを忘れない
        self.assertContains(response, "コメント投稿", status_code=200)

    def test_create_comment(self):
        data = {"text": "comment11"}
        self.client.post(f"/snippets/{self.snippet.id}/comments/new/", data)
        comment = Comment.objects.get(text="comment11")
        self.assertEqual(self.snippet, comment.commented_to)  # これ引数の順番大事？
        self.assertEqual(self.user, comment.commented_by)
