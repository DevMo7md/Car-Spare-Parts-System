# Generated by Django 5.1.3 on 2024-12-15 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CSP_app', '0007_alter_supplier_created_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='created_date',
            new_name='created_at',
        ),
    ]
