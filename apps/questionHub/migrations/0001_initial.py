# Generated by Django 5.0.6 on 2024-05-23 20:56

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Було створено')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Закладка',
                'verbose_name_plural': 'Закладки',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='url')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Деталі')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Було створено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Було оновлено')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Чи закрито')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('bookmarks', models.ManyToManyField(related_name='bookmarked_questions', through='questionHub.Bookmark', to=settings.AUTH_USER_MODEL, verbose_name='Закладки')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='questionHub.category', verbose_name='Категорія')),
            ],
            options={
                'verbose_name': 'Питання',
                'verbose_name_plural': 'Питання',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='bookmark',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked_by', to='questionHub.question', verbose_name='Питання'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Деталі')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Було створено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Було оновлено')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='questionHub.question', verbose_name='Питання')),
            ],
            options={
                'verbose_name': 'Відповідь',
                'verbose_name_plural': 'Відповіді',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together={('user', 'question')},
        ),
    ]
