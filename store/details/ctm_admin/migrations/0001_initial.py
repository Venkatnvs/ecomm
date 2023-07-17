# Generated by Django 4.1.6 on 2023-07-17 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0007_alter_product_subcategories'),
        ('clients', '0010_remove_customeruser_api_delete_userapikey'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.selleruser')),
            ],
        ),
    ]
