# Generated by Django 5.0.7 on 2024-08-27 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0008_rename_userprofile_userprofilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='image',
            field=models.ImageField(default='householdImages/defaultImage.png', upload_to='householdImages'),
        ),
        migrations.AlterField(
            model_name='userprofilepic',
            name='image',
            field=models.ImageField(default='userImage/defaultImage.png', upload_to='userImage'),
        ),
    ]
