# Generated by Django 4.1 on 2022-09-09 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('on_time', models.DateTimeField()),
                ('sent', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-on_time'],
            },
        ),
    ]
