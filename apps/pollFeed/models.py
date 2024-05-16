from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class PollCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Answer(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, related_name='answers')
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.content

    class Meta:
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді'


class Poll(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    category = models.ForeignKey(PollCategory, on_delete=models.CASCADE, related_name='polls')
    question = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.question

    class Meta:
        verbose_name = 'Опитування'
        verbose_name_plural = 'Опитування'


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_answers')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='poll_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='poll_answers')

    def __str__(self):
        return f"{self.user.username}'s answer to {self.poll} - {self.answer}"

    class Meta:
        verbose_name = 'Відповідь користувача'
        verbose_name_plural = 'Відповіді користувачів'
