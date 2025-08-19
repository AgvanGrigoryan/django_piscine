from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.db.models.signals import post_delete, post_save
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Tip

User = get_user_model()

@receiver(post_delete, sender=Tip)
def tip_delete_handler(sender, instance, **kwargs):
    instance.author.recalc_reputation()

@receiver(post_save, sender=User)
def update_user_permissions(sender, instance, created, **kwargs):
    if not instance.pk:
        return
    
    try:
        can_delete = Permission.objects.get(codename='can_delete_tips')
        can_downvote = Permission.objects.get(codename='can_downvote')
    except Permission.DoesNotExist:
        return
    
    if instance.reputation >= settings.REPUTATION_DELETE_UNLOCK:
        instance.user_permissions.add(can_delete)
    else:
        instance.user_permissions.remove(can_delete)

    if instance.reputation >= settings.REPUTATION_DOWNVOTE_UNLOCK:
        instance.user_permissions.add(can_downvote)
    else:
        instance.user_permissions.remove(can_downvote)
