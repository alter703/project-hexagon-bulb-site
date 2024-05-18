# Generated by Django 5.0.6 on 2024-05-18 11:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollFeed', '0003_alter_choice_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='author',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, related_name='choices', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poll',
            name='author',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='polls', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='pollFeed.poll'),
        ),
    ]
