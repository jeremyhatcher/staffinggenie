# Generated by Django 4.1.6 on 2023-03-29 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Opportunities', '0004_rename_is_slotter_customuser_is_receiving_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_receiving',
            new_name='is_receiver',
        ),
    ]
