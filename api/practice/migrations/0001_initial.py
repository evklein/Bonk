# Generated by Django 5.0.6 on 2024-07-06 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('game_type', models.CharField(max_length=50)),
                ('game_data', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PracticeStroke',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_time', models.DateTimeField(auto_now_add=True)),
                ('shot_type', models.CharField(max_length=50)),
                ('shot_distance', models.IntegerField()),
                ('result_side', models.CharField(max_length=50)),
                ('result_distance', models.CharField(max_length=50)),
                ('result_shape_direction', models.CharField(blank=True, max_length=50, null=True)),
                ('result_shape', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]