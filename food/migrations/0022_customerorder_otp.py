# Generated by Django 3.1.6 on 2021-03-22 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0021_auto_20210322_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='OTP',
            field=models.IntegerField(default=1635, null=True),
        ),
    ]