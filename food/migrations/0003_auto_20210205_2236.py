# Generated by Django 3.1.6 on 2021-02-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_customerorder_product_shop_shoplocality'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='delivered',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='customerorder',
            name='onTheWay',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
