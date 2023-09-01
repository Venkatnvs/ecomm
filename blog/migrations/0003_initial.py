# Generated by Django 4.0.7 on 2023-08-29 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0011_alter_selleruser_company_name'),
        ('blog', '0002_delete_blogpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, help_text='Unique and created from name', max_length=250, null=True, unique=True)),
                ('image', models.ImageField(upload_to='blog/categories/uploads/%Y/%m/%d/')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('meta_keywords', models.CharField(help_text='Comma seperated set of SEO Keywords for meta tag', max_length=255, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(help_text='Content for description of meta tag', max_length=255, verbose_name='Meta Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='blog name', max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, help_text='Unique and created from name', max_length=255, null=True, unique=True)),
                ('brand', models.CharField(help_text='Unique Brand name', max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('long_description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('only_registered', models.BooleanField(default=False)),
                ('add_slider', models.BooleanField(default=False)),
                ('add_picks', models.BooleanField(default=False)),
                ('is_trending', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('meta_keywords', models.CharField(help_text='Comma seperated set of SEO Keywords for meta tag', max_length=255, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(help_text='Content for description of meta tag', max_length=255, verbose_name='Meta Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.customer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BlogTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogs')),
            ],
        ),
        migrations.CreateModel(
            name='BlogSubCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, help_text='Unique and created from name', max_length=250, null=True, unique=True)),
                ('image', models.ImageField(upload_to='blog/categories/subcategory/uploads/%Y/%m/%d/')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('meta_keywords', models.CharField(help_text='Comma seperated set of SEO Keywords for meta tag', max_length=255, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(help_text='Content for description of meta tag', max_length=255, verbose_name='Meta Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogcategories')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='blogs',
            name='subcategories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogsubcategories'),
        ),
        migrations.CreateModel(
            name='BlogMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Image', 'Image'), ('Video', 'Video'), ('File', 'File')], default='Image', max_length=255)),
                ('content', models.FileField(upload_to='blog/media/uploads/%Y/%m/%d/')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('blog_inside', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogs')),
            ],
        ),
    ]