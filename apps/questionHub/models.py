import uuid
from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse, reverse_lazy

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

class Question(models.Model):
    slug = models.SlugField(max_length=255, default=uuid.uuid4, unique=True, verbose_name='url')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_closed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'

    def get_absolute_url(self):
        return reverse_lazy("questionHub:detail", kwargs={"slug": self.slug})


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді' 