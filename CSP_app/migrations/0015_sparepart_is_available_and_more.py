# Generated by Django 5.1.3 on 2025-03-07 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSP_app', '0014_incomebillitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparepart',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='sparepart',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
