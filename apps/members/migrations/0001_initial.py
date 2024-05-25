# Generated by Django 5.0.6 on 2024-05-23 20:56

import django.db.models.deletion
import imagekit.models.fields
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
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('biography', models.TextField(blank=True, max_length=255, null=True, verbose_name='Біографія')),
                ('avatar', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Зображення')),
                ('joined_at', models.DateTimeField(auto_now_add=True, verbose_name='Приєднався')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Профіль',
                'verbose_name_plural': 'Профілі',
                'ordering': ('user',),
            },
        ),
    ]
