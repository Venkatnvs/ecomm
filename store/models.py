from django.db import models
from clients.models import SellerUser, CustomerUser
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Unique and created from name", max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='categories/uploads/%Y/%m/%d/')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text="Comma seperated set of SEO Keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255, help_text="Content for description of meta tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('admin-categorylist')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Unique and created from name", max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='categories/subcategory/uploads/%Y/%m/%d/')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text="Comma seperated set of SEO Keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255, help_text="Content for description of meta tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Subcategories'

    def get_absolute_url(self):
        return reverse('admin-subcategorylist')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text='product name')
    slug = models.SlugField(max_length=255, unique=True, help_text="Unique and created from name", null=True, blank=True)
    brand = models.CharField(max_length=255, unique=True, help_text="Unique Brand name")
    subcategories = models.OneToOneField(SubCategory, null=True, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, null=True, blank=True)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    offer = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    new_price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    long_description = models.TextField()
    by_seller = models.ForeignKey(SellerUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/uploads/%Y/%m/%d/')
    is_active = models.BooleanField(default=True)
    is_bestselling = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False, help_text="No shipping required (ex: online book pdf)")
    return_allowed = models.BooleanField(default=False)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text="Comma seperated set of SEO Keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255, help_text="Content for description of meta tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductMedia(models.Model):
    media_type = (
        (1,"Image"),
        (2,"Video")
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=media_type)
    content = models.FileField(upload_to="products/media/uploads/%Y/%m/%d/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class ProductTransaction(models.Model):
    transaction_type = (
        (1,"Buy"),
        (2,"Sell")
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    type = models.CharField(max_length=255, choices=transaction_type)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class ProductDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    details = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class ProductAbout(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class ProductTags(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class ProductQuestions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class ProductReviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    rating = models.CharField(max_length=100, default="5")
    review = models.TextField(default="")
    media = models.FileField(upload_to="products/review/uploads/%Y/%m/%d/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

class ProductReviewsVoting(models.Model):
    product_review = models.ForeignKey(ProductReviews, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    voting = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_review.product.name


class ProductVarient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProductVarientItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_varient = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title