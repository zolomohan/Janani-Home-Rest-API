# Generated by Django 3.0.6 on 2020-05-09 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
