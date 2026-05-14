# pyrefly: ignore [missing-import]
from django.db.models.signals import m2m_changed
# pyrefly: ignore [missing-import]
from django.dispatch import receiver
# pyrefly: ignore [missing-import]
from .models import Image

@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
