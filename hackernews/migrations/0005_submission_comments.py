# Generated by Django 4.0.3 on 2022-04-05 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0004_submission_author_submission_points_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='comments',
            field=models.IntegerField(default=0),
        ),
    ]
