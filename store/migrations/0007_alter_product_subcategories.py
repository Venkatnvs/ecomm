# Generated by Django 4.0.7 on 2022-10-21 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.subcategory'),
        ),
    ]