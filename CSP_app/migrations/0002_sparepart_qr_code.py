# Generated by Django 5.1.3 on 2024-11-29 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSP_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparepart',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes'),
        ),
    ]
