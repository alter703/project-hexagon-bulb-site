import uuid

from django.db import models

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, SmartCrop


# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(null=True, blank=True)
    avatar = ProcessedImageField(
        upload_to='avatars/',
        processors=[ResizeToFill(550, 550)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
        null=True)
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(250, 250)],
        format='WEBP',
        options={'quality': 60},
    )

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
        
    