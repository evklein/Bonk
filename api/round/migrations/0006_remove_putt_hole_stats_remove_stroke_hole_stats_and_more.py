# Generated by Django 5.0.6 on 2024-06-29 01:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_alter_tee_rating_alter_tee_slope'),
        ('round', '0005_stroke_penalty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='putt',
            name='hole_stats',
        ),
        migrations.RemoveField(
            model_name='stroke',
            name='hole_stats',
        ),
        migrations.AddField(
            model_name='putt',
            name='hole',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='course.hole'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='putt',
            name='rnd',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='round.round'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stroke',
            name='hole',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='course.hole'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stroke',
            name='rnd',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='round.round'),
            preserve_default=False,
        ),
    ]
