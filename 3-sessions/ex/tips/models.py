from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Tip(models.Model):
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tips')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        permissions = [
            ('can_downvote', 'Can downvote tips'),
            ('can_delete_tips', 'Can delete tips'),
        ]

    def __vote(self, user, vote_type: bool):
        try:
            vote = self.votes.get(user=user)
            if vote.is_upvoted != vote_type:
                vote.is_upvoted = vote_type
                vote.save()
            else:
                vote.delete()
        except Vote.DoesNotExist:
            self.votes.create(tip=self, user=user, is_upvoted=vote_type)

    def upvote(self, user):
        self.__vote(user, True)

    def downvote(self, user):
        self.__vote(user, False)

    def remove_vote(self, user):
        self.votes.filter(user=user).delete()

    def upvotes_count(self):
        self.votes.filter(is_upvoted=True).count()

    def downvotes_count(self):
        self.votes.filter(is_upvoted=False).count()

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, related_name='votes')
    is_upvoted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'tip')