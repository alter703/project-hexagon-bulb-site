import uuid
from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse, reverse_lazy

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Question(models.Model):
    id = models.UUIDField(max_length=255, default=uuid.uuid4, unique=True, editable=False, primary_key=True, verbose_name='url')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions', verbose_name='Категорія')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Деталі')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Було створено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Було оновлено')

    is_closed = models.BooleanField(default=False, verbose_name='Чи закрито')
    bookmarks = models.ManyToManyField(User, through='Bookmark', related_name='bookmarked_questions', verbose_name='Закладки')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'

    def get_absolute_url(self):
        return reverse_lazy("questionHub:detail", kwargs={"id": self.id})


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', verbose_name='Автор')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Питання')
    content = models.TextField(verbose_name='Деталі')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Було створено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Було оновлено')


    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді'


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='Користувач')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='bookmarked_by', verbose_name='Питання')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Було створено')

    class Meta:
        unique_together = ('user', 'question')
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"
