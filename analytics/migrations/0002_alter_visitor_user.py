# Generated by Django 4.0.7 on 2023-09-12 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='user',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
