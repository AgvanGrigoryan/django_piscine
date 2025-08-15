from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Tip(models.Model):
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)