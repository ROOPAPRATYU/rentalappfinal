# Generated by Django 4.1.7 on 2023-03-13 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propertyManager', '0007_alter_propertydetail_adhar_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertydetail',
            name='adhar_pic',
            field=models.FileField(blank=True, upload_to='adhar_card'),
        ),
    ]