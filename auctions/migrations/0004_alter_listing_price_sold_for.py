# Generated by Django 3.2.7 on 2021-12-12 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211211_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price_sold_for',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
