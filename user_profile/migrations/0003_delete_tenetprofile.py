# Generated by Django 4.1.7 on 2023-03-17 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_remove_ownerprofile_age'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TenetProfile',
        ),
    ]
