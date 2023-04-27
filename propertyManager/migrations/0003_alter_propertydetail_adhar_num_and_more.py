# Generated by Django 4.1.7 on 2023-03-13 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propertyManager', '0002_propertydetail_is_property_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertydetail',
            name='adhar_num',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='propertydetail',
            name='age',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='propertydetail',
            name='bhk',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='propertydetail',
            name='phone_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='propertydetail',
            name='rent_due_date',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='propertydetail',
            name='tenant_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]