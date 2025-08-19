from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0, help_text="Reputation points")

    def add_reputation(self, points: int):
        self.reputation += points
        self.save(update_fields=['reputation'])

    def recalc_reputation(self):
        agg = self.tips.aggregate(
            upvotes=models.Count('votes', filter=models.Q(votes__is_upvoted=True)),
            downvotes=models.Count('votes', filter=models.Q(votes__is_upvoted=False)),
        )

        self.reputation = (
            agg['upvotes'] * settings.REPUTATION_UPVOTE_POINTS +
            agg['downvotes'] * settings.REPUTATION_DOWNVOTE_POINTS
        )
        self.save(update_fields=['reputation'])
