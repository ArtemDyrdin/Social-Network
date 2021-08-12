from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Friends(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    friend = models.IntegerField()

    def __str__(self):
        return self.friend

    def get_absolute_url(self):
        return '/friends'

    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.BooleanField('theme', default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(author=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
