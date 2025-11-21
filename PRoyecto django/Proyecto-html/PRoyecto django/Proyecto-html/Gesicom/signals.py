from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_migrate)
def ensure_groups(sender, **kwargs):
    for name in ["usuario", "instructor", "investigador", "dinamizador", "coordinador"]:
        Group.objects.get_or_create(name=name)

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name="usuario")
        instance.groups.add(group)