from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from articles.models import Article, UserFavouriteArticle

User = get_user_model()

class FavouritesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testuserpass123!!!')
        cls.user2 = User.objects.create_user(username='testuser2', password='testuserpass123!!!')

    def setUp(self):
        login = self.client.login(username='testuser', password='testuserpass123!!!')
        self.assertTrue(login)

    def test_add_article_to_favourites(self):
        """Авторизованный пользователь может добавить статью в избранное"""
        article = Article.objects.create(
            title="Test Article",
            synopsis="Summary",
            content="Content",
            author=self.user2
        )
        response = self.client.post(
            reverse('add-favourite', kwargs={'pk': article.pk}),
            data={'article': article.pk}
        )
        self.assertRedirects(response, reverse('article-detail', kwargs={'pk': article.pk}))
        self.assertEqual(
            UserFavouriteArticle.objects.filter(user=self.user, article=article).count(),
            1
        )

    def test_cannot_add_same_article_twice(self):
        """Нельзя добавить одну и ту же статью дважды в избранное"""
        article = Article.objects.create(
            title="Test Article",
            synopsis="Summary",
            content="Content",
            author=self.user2
        )

        self.client.post(
            reverse('add-favourite', kwargs={'pk': article.pk}),
            data={'article': article.pk}
        )
        response = self.client.post(
            reverse('add-favourite', kwargs={'pk': article.pk}),
            data={'article': article.pk}
        )
        self.assertRedirects(response, reverse('article-detail', kwargs={'pk': article.pk}))
        self.assertEqual(
            UserFavouriteArticle.objects.filter(user=self.user, article=article).count(),
            1
        )

    def test_favourite_article_shows_in_list(self):
        """Добавленная в избранное статья отображается в списке избранного"""
        article = Article.objects.create(
            title="Test Article",
            synopsis="Summary",
            content="Content",
            author=self.user2
        )
        UserFavouriteArticle.objects.create(user=self.user, article=article)
        response = self.client.get(reverse('favourites'))
        self.assertContains(response, article.title)
