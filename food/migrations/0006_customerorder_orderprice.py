# Generated by Django 3.1.6 on 2021-02-10 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_shop_locality'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='orderPrice',
            field=models.FloatField(default=100),
        ),
    ]