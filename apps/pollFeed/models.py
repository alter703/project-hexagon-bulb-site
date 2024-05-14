from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class PollCategory(models.Model):
    pass


class Poll(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    category = models.ForeignKey(PollCategory, on_delete=models.CASCADE, related_name='polls')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title