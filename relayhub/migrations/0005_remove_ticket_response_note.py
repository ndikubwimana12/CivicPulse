# Generated by Django 5.2 on 2025-05-17 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relayhub', '0004_category_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='response_note',
        ),
    ]
