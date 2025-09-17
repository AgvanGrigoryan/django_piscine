from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from articles.models import Article

User = get_user_model()

class UnauthorizedAccessControlTestCase(TestCase):
    def test_publish_redirects_for_anonymous(self):
        url = reverse('publish')
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('login-view') + f'?next={url}'
        )

    def test_publish_post_redirects_for_anonymous(self):
        data = {
            'title': 'Test Article',
            'synopsis': 'Short summary',
            'content': 'Full content of the article',
        }
        url = reverse('publish')
        response = self.client.post(url, data)
        self.assertRedirects(
            response,
            reverse('login-view') + f'?next={url}'
        )

    def test_user_articles_list_redirects_for_anonymous(self):
        url = reverse('my-articles')
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('login-view') + f'?next={url}'
        )

    def test_favorites_list_redirects_for_anonymous(self):
        url = reverse('favourites')
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('login-view') + f'?next={url}'
        )

    def test_add_to_favorites_redirects_for_anonymous(self):
        url = reverse('add-favourite', kwargs={'pk': 8})
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('login-view') + f'?next={url}'
        )

class AuthorizedAccessControlTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testuserpass123!!!')
        article = Article.objects.create(
            title='This is test article 1',
            synopsis='This is short description of article 1',
            content='This is content of article 1',
            author=cls.user
        )
        cls.articles_list = [article]

    def setUp(self):
        login = self.client.login(username='testuser', password='testuserpass123!!!')
        self.assertTrue(login)

    # def test_user_exists(self):
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(self.user.username, "testuser")

    def test_publish_accessible_for_authenticated(self):
        url = reverse('publish')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200
        )

    def test_user_articles_list_accessible_for_authenticated(self):
        url = reverse('my-articles')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200
        )

    def test_favorites_list_accessible_for_authenticated(self):
        url = reverse('favourites')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200
        )

    def test_add_to_favorites_accessible_for_authenticated(self):
        article = self.articles_list[0] if self.articles_list else 0
        url = reverse('add-favourite', kwargs={'pk': article.pk})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_registration_page_redirects_for_authenticated(self):
        url = reverse('register-view')
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('home-view'),
            fetch_redirect_response=False
        )