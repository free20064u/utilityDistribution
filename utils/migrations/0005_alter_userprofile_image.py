# Generated by Django 5.0.7 on 2024-08-15 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_alter_household_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='userImage/defaultImage.jpg', upload_to='userImage'),
        ),
    ]
