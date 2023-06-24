from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os

from ckeditor_uploader.fields import RichTextUploadingField

@receiver(post_delete, sender=RichTextUploadingField)
def delete_image(sender, instance, **kwargs):
    if instance:
        if os.path.isfile(instance.path):
            os.remove(instance.path)
