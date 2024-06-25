# Generated by Django 4.2.13 on 2024-06-24 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('round', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='putt',
            old_name='stroke',
            new_name='stroke_number',
        ),
        migrations.RenameField(
            model_name='round',
            old_name='tees',
            new_name='played_tee',
        ),
        migrations.RenameField(
            model_name='stroke',
            old_name='stroke',
            new_name='stroke_number',
        ),
        migrations.AddField(
            model_name='round',
            name='finish_time',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='group_makeup',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='holes_completed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='round',
            name='mobility',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='notes',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='round_counts_toward_hci',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='round',
            name='tee_time',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
