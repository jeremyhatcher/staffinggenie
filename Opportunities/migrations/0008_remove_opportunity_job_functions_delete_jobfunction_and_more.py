# Generated by Django 4.1.6 on 2023-03-29 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Opportunities', '0007_jobfunction_opportunity_total_slots_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opportunity',
            name='job_functions',
        ),
        migrations.DeleteModel(
            name='JobFunction',
        ),
        migrations.AddField(
            model_name='opportunity',
            name='job_functions',
            field=models.CharField(choices=[('Unloading', 'Unloading'), ('Loading', 'Loading'), ('Pallet Picking', 'Pallet Picking'), ('Reserve Picking', 'Reserve Picking'), ('Receiving', 'Receiving'), ('Yard Driving', 'Yard Driving'), ('Desk Clerking', 'Desk Clerking'), ('QA', 'QA'), ('Office Admin', 'Office Admin'), ('AP', 'AP')], default='Unloading', max_length=255),
            preserve_default=False,
        ),
    ]