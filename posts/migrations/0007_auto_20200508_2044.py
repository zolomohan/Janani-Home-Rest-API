# Generated by Django 3.0.6 on 2020-05-08 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_dislike_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='not_recommended',
        ),
        migrations.RemoveField(
            model_name='post',
            name='recommended',
        ),
    ]
