# Generated by Django 3.1.6 on 2021-03-18 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0016_auto_20210318_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='food.shop'),
        ),
    ]