from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User


# Create your models here.
class Poll(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Голосування'
        verbose_name_plural = 'Голосування'

    def get_absolute_url(self):
        return reverse_lazy("questionHub:detail", kwargs={"id": self.id})


class Choice(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='choices')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)


    class Meta:
        ordering = ('-votes',)
        verbose_name = 'Вибір'
        verbose_name_plural = 'Вибори'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='user_votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='user_votes')

    class Meta:
        unique_together = ('user', 'poll')
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоси'
