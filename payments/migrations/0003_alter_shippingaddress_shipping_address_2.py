# Generated by Django 5.1.1 on 2024-10-07 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_rename_address_1_shippingaddress_shipping_address_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_address_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
