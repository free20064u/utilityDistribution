# Generated by Django 5.0.7 on 2024-08-26 21:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0007_alter_userprofile_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='UserProfilePic',
        ),
    ]
