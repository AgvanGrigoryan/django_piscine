from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from articles.models import Article

User = get_user_model()

class PublicationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testuserpass123!!!')
        cls.user2 = User.objects.create_user(username='testuser2', password='testuserpass123!!!')

    def setUp(self):
        login = self.client.login(username='testuser', password='testuserpass123!!!')

    def test_publish_article_success(self):
        """Залогиненный пользователь может создать статью, редирект на my-articles"""
        data = {
            'title': 'Test Article',
            'synopsis': 'Short summary',
            'content': 'Full content of the article',
        }
        response = self.client.post(reverse('publish'), data)
        
        self.assertRedirects(response, reverse('my-articles'))

        article = Article.objects.get(title='Test Article')
        self.assertEqual(article.author, self.user)

    def test_article_list_initially_empty(self):
        response = self.client.get(reverse('article-list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['articles'], [])

    def test_adding_articles_and_list_shows_published_articles(self):
        """Список статей отображает опубликованные статьи"""
        data = {
            'title': 'Test Article1',
            'synopsis': 'Short summary 1',
            'content': 'Full content of the article 1',
        }
        response = self.client.post(reverse('publish'), data)

        data = {
            'title': 'Test Article2',
            'synopsis': 'Short summary 2',
            'content': 'Full content of the article 2',
        }
        response = self.client.post(reverse('publish'), data)

        response = self.client.get(reverse('article-list'))
        self.assertEqual(response.status_code, 200)
        articles = response.context['articles']
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, 'Test Article2')
        self.assertEqual(articles[1].title, 'Test Article1')

    def test_article_list_view_ordering(self):
        """Статьи в общем списке выводятся в правильном порядке (например, новые первыми)"""
        data = {
            'title': 'Test Article1',
            'synopsis': 'Short summary 1',
            'content': 'Full content of the article 1',
        }
        response = self.client.post(reverse('publish'), data)

        data = {
            'title': 'Test Article2',
            'synopsis': 'Short summary 2',
            'content': 'Full content of the article 2',
        }
        response = self.client.post(reverse('publish'), data)

        response = self.client.get(reverse('article-list'))
        self.assertEqual(response.status_code, 200)
        articles = response.context['articles']
        self.assertTrue(
            all(articles[i].created >= articles[i+1].created for i in range(len(articles) - 1))
        )
  
    def test_my_articles_shows_only_user_articles(self):
        """В 'my-articles' отображаются только статьи текущего пользователя"""
        article = Article.objects.create(
            title='Article by Other',
            synopsis='Summary',
            content='Content of article',
            author=self.user2
        )
        data = {
            'title': 'My Article',
            'synopsis': 'Short summary',
            'content': 'Full content of the article',
        }
        response = self.client.post(reverse('publish'), data)

        response = self.client.get(reverse('my-articles'))
        self.assertEqual(response.status_code, 200)
        articles = response.context['articles']
        self.assertTrue(
            all(article.author == self.user for article in articles)
        )

    def test_article_detail_view_accessible(self):
        """Детальная страница статьи доступна и возвращает 200"""
        article = Article.objects.create(
            title='Article by Other',
            synopsis='Summary',
            content='Content of article',
            author=self.user2
        )
        response = self.client.get(reverse('article-detail', kwargs={'pk':article.pk}))
        self.assertEqual(response.status_code, 200)

    def test_article_detail_view_not_found_for_invalid_id(self):
        """Запрос несуществующей статьи возвращает 404"""
        response = self.client.get(reverse('article-detail', kwargs={'pk':7777}))
        self.assertEqual(response.status_code, 404)

    def test_publish_article_form_validation(self):
        """Форма создания статьи возвращает ошибки при отсутствии обязательных полей"""
        
        # Форма должна вернуться с кодом 200
        response = self.client.post(reverse('publish'), data={})

        # Форма должна вернуться с кодом 200
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertTrue(form.errors)  # Ошибки есть
        self.assertIn('title', form.errors)
        self.assertIn('synopsis', form.errors)