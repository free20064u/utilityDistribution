# Generated by Django 5.0.7 on 2024-07-27 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_alter_appliance_power'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='credit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
