# Generated by Django 3.2 on 2022-06-02 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_dashboard', '0002_workreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectActivitiesDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proj_name', models.CharField(max_length=500)),
                ('activities', models.CharField(blank=True, max_length=500)),
                ('activity_start_date', models.CharField(blank=True, max_length=500)),
                ('activity_end_date', models.CharField(blank=True, max_length=500)),
                ('working_days', models.CharField(blank=True, max_length=500)),
                ('status', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.DeleteModel(
            name='ProjectFeaturesDetail',
        ),
    ]
