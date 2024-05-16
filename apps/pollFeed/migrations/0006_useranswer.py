# Generated by Django 5.0.6 on 2024-05-16 05:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollFeed', '0005_delete_pollanswer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_who_chose', to='pollFeed.answer')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='pollFeed.poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chosen_answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]