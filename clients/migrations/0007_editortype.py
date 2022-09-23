# Generated by Django 4.1 on 2022-09-07 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_adminuser_city_adminuser_state_adminuser_zip_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editor', models.CharField(choices=[('TinyMCE', 'TinyMCE'), ('Ckeditor4', 'Ckeditor4')], default='TinyMCE', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
