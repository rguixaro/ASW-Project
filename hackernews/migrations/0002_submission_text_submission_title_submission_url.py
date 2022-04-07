# Generated by Django 4.0.3 on 2022-03-24 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='text',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='submission',
            name='url',
            field=models.CharField(default='', max_length=50),
        ),
    ]
