# Generated by Django 4.1.6 on 2023-07-16 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0010_remove_customeruser_api_delete_userapikey'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(upload_to='Customer/SellerUser/Staff/%Y/%m/%d/')),
                ('customer_type', models.CharField(choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Employ', 'Employ')], default='Employ', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clients.selleruser')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]