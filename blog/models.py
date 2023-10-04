from django.db import models
from clients.models import Customer
from django.urls import reverse

class BlogCategories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Unique and created from name", max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='blog/categories/uploads/%Y/%m/%d/')
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text="Comma seperated set of SEO Keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255, help_text="Content for description of meta tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def img_url(self):
        try:
            url = self.image.url
        except:
            url = '/static/main/img/no-image.jpg'
        return url

    def get_absolute_url(self):
        return reverse('admin-categorylist')

    def __str__(self):
        return self.name


class BlogSubCategories(models.Model):
    category = models.ForeignKey(BlogCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Unique and created from name", max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='blog/categories/subcategory/uploads/%Y/%m/%d/')
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text="Comma seperated set of SEO Keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255, help_text="Content for description of meta tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def img_url(self):
        try:
            url = self.image.url
        except:
            url = '/static/main/img/no-image.jpg'
        return url

    def get_absolute_url(self):
        return reverse('admin-subcategorylist')

    def __str__(self):
        return self.name


class Blogs(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text='blog name')
    slug = models.SlugField(max_length=255, unique=True, help_text="Unique and created from name", null=True, blank=True)
    brand = models.CharField(max_length=255, unique=True, help_text="Unique Brand name")
    subcategories = models.ForeignKey(BlogSubCategories, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    long_description = models.TextField()
    by_user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    only_registered = models.BooleanField(default=False)
    add_slider = models.BooleanField(default=False)
    add_picks = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text="Comma seperated set of SEO Keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255, help_text="Content for description of meta tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def first_img(self):
        try:
            img_url = BlogMedia.objects.filter(blog=self,is_active=True,type=1).first()
            url = img_url.img_url
        except:
            url = '/static/main/img/no-image.jpg'
        return url

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
class BlogMedia(models.Model):
    media_type = (
        ("Image","Image"),
        ("Video","Video"),
        ("File","File")
    )
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=media_type,default="Image")
    content = models.FileField(upload_to="blog/media/uploads/%Y/%m/%d/")
    image_url = models.URLField(null=True, blank=True)
    blog_inside = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def img_url(self):
        try:
            if self.content:
                rl = self.content.url
            elif self.image_url:   # Check if there's an image URL
                url = self.image_url
            else:
                url = '/static/main/img/no-image.jpg'
        except:
            url = '/static/main/img/no-image.jpg'
        return url

    def __str__(self):
        return self.blog.name
    
class BlogTags(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog.name