# Generated by Django 4.2 on 2023-11-13 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_apply_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='apply_followers',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_apply_followers',
            field=models.BooleanField(default=False),
        ),
    ]
