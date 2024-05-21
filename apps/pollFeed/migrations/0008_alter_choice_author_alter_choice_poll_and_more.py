# Generated by Django 5.0.6 on 2024-05-19 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollFeed', '0007_alter_vote_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='pollFeed.poll', verbose_name='Голосування'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=255, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0, verbose_name='Голосів'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polls', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Було створено'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Чи закрито'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='text',
            field=models.CharField(max_length=255, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_votes', to='pollFeed.choice', verbose_name='Вибір'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_votes', to='pollFeed.poll', verbose_name='Голосування'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_votes', to=settings.AUTH_USER_MODEL, verbose_name='Користувач'),
        ),
    ]