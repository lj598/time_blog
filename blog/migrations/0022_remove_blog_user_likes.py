# Generated by Django 3.1.3 on 2021-01-30 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20210130_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='user_likes',
        ),
    ]