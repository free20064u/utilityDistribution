# Generated by Django 5.0.7 on 2024-08-02 02:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0006_remove_household_credit_debt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='debt',
            old_name='credit',
            new_name='totalDept',
        ),
    ]
