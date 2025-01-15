# Generated by Django 5.1.4 on 2025-01-14 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board1', '0004_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('price', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]