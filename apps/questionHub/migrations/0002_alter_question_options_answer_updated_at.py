# Generated by Django 5.0.6 on 2024-05-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionHub', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='answer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
