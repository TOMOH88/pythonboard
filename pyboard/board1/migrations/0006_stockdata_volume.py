# Generated by Django 5.1.4 on 2025-01-14 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board1', '0005_stockdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockdata',
            name='volume',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
