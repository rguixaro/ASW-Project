# Generated by Django 4.0.3 on 2022-04-17 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0014_action'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='points',
        ),
    ]