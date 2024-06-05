import uuid

from django.db import models

from django.urls import reverse, reverse_lazy
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, SmartCrop


# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile', verbose_name='Користувач')
    biography = models.TextField(null=True, blank=True, max_length=255, verbose_name='Біографія')
    avatar = ProcessedImageField(
        upload_to='avatars/',
        processors=[ResizeToFill(550, 550)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
        null=True, verbose_name='Зображення')
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(250, 250)],
        format='WEBP',
        options={'quality': 60},
    )

    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='Приєднався')

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ('user',)
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 'https://www.gravatar.com/avatar/{}?d=identicon'.format(self.user.username)

    def get_avatar_thumbnail(self):
        if self.avatar_thumbnail:
            return self.avatar_thumbnail.url
        else:
            return 'https://www.gravatar.com/avatar/{}?d=identicon'.format(self.user.username)

    def get_absolute_url(self):
        return reverse_lazy("members:profile", kwargs={"id": self.id})
