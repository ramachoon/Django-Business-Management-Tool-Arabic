from os import getcwd, remove
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User


@receiver(post_delete, sender=User)
def delete_user_avatar_after_delete(sender, instance, *args, **kwargs):
    path = getcwd()
    final_path = path + instance.avatar.url
    if final_path.split('/')[-1] != 'default.jpg':
        remove(final_path)
