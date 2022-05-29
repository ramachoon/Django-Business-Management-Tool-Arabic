from os import getcwd, remove
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Kala


@receiver(post_delete, sender=Kala)
def delete_kala_qr_image_after_delete(sender, instance, *args, **kwargs):
    path = getcwd()
    final_path = path + instance.qr_image.url
    remove(final_path)
