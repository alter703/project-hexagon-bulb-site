import uuid
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User


# Create your models here.
class Poll(models.Model):
    STATUS_POLL_CHOICES = (
        (True, 'Закрито'),
        (False, 'Відкрито'),
    )
    
    id = models.UUIDField(max_length=255, default=uuid.uuid4, unique=True, editable=False, primary_key=True, verbose_name='url')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls', verbose_name='Автор')
    text = models.CharField(max_length=255, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Було створено')
    is_closed = models.BooleanField(default=False, verbose_name='Чи закрито', choices=STATUS_POLL_CHOICES)

    def __str__(self) -> str:
        return self.text
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Голосування'
        verbose_name_plural = 'Голосування'

    def get_absolute_url(self):
        return reverse_lazy("pollFeed:detail", kwargs={"id": self.id})


class Choice(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='choices', verbose_name='Автор')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices', verbose_name='Голосування')
    text = models.CharField(max_length=255, verbose_name='Текст')
    votes = models.IntegerField(default=0, verbose_name='Голосів')


    class Meta:
        ordering = ('-votes',)
        verbose_name = 'Вибір'
        verbose_name_plural = 'Вибори'

    def __str__(self) -> str:
        return self.text

class Vote(models.Model):
    STATUS_VOTE_CHOICES = (
        (True, 'Так'),
        (False, 'Ні'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes', verbose_name='Користувач', null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='user_votes', verbose_name='Голосування')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='user_votes', verbose_name='Вибір')

    is_anonymous = models.BooleanField(default=False, verbose_name='Чи анонімний голос', choices=STATUS_VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'poll')
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоси'

    def __str__(self):
        return f"Vote by {self.user if self.user else 'Anonymous'} on {self.poll}"
