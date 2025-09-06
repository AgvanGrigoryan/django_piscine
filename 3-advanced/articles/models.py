from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Article(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=False)
    synopsis = models.CharField(max_length=312)
    content = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.title

class UserFavouriteArticle(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite_articles'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='favourited_by'
    )

    def __str__(self):
        return self.article.title

    class Meta:
        unique_together = ('user', 'article')