from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save


class Customer(models.Model):
    customer_type_choices = (
        ("Admin","Admin"),
        ("Staff","Staff"),
        ("Seller","Seller"),
        ("Customer","Customer")
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=100, choices=customer_type_choices, default="Customer")

    @property
    def img_url(self):
        url = '/static/main/img/default-user.jpg'
        if self.customer_type == "Admin":
            try:
                url = self.adminuser.profile_pic.url
            except:
                url = '/static/main/img/default-user.jpg'
        if self.customer_type == "Staff":
            try:
                url = self.staffuser.profile_pic.url
            except:
                url = '/static/main/img/default-user.jpg'
        if self.customer_type == "Seller":
            try:
                url = self.selleruser.profile_pic.url
            except:
                url = '/static/main/img/default-user.jpg'
        if self.customer_type == "Customer":
            try:
                url = self.customeruser.profile_pic.url
            except:
                url = '/static/main/img/default-user.jpg'
        return url

    def __str__(self):
        return self.user.username + ' ~' + self.customer_type

class AdminUser(models.Model):
    user_type = models.OneToOneField(Customer, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Customer/AdminUser/%Y/%m/%d/')
    address = models.TextField(default="")
    state = models.CharField(max_length=255, default="")
    city = models.CharField(max_length=255, default="")
    zip = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def img_url(self):
        try:
            url = self.profile_pic.url
        except:
            url = '/static/main/img/default-user.jpg'
        return url

    def __str__(self):
        return self.user_type.user.username

class CustomerUser(models.Model):
    user_type = models.OneToOneField(Customer, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Customer/CustomerUser/%Y/%m/%d/')
    address = models.TextField(default="")
    state = models.CharField(max_length=255, default="")
    city = models.CharField(max_length=255, default="")
    zip = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def img_url(self):
        try:
            url = self.profile_pic.url
        except:
            url = '/static/main/img/default-user.jpg'
        return url

    def __str__(self):
        return self.user_type.user.username

class StaffUser(models.Model):
    user_type = models.OneToOneField(Customer, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Customer/StaffUser/%Y/%m/%d/')
    address = models.TextField(default="")
    state = models.CharField(max_length=255, default="")
    city = models.CharField(max_length=255, default="")
    zip = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def img_url(self):
        try:
            url = self.profile_pic.url
        except:
            url = '/static/main/img/default-user.jpg'
        return url

    def __str__(self):
        return self.user_type.user.username

class SellerUser(models.Model):
    user_type = models.OneToOneField(Customer, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Customer/SellerUser/%Y/%m/%d/')
    company_name = models.CharField(max_length=255, default="",unique=True)
    gst_details = models.CharField(max_length=255, default="")
    address = models.TextField(default="")
    state = models.CharField(max_length=255, default="")
    city = models.CharField(max_length=255, default="")
    zip = models.CharField(max_length=255, default="")
    by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def img_url(self):
        try:
            url = self.profile_pic.url
        except:
            url = '/static/main/img/default-user.jpg'
        return url

    def __str__(self):
        return self.user_type.user.username

class EditorType(models.Model):
    editor_type_choices = (
        ("TinyMCE","TinyMCE"),
        ("Ckeditor4","Ckeditor4")
    )
    editor = models.CharField(max_length=255, choices=editor_type_choices, default="TinyMCE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.editor

@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.customer_type == "Admin":
            admin = AdminUser.objects.create(user_type=instance)
            admin.save()
        if instance.customer_type == "Staff":
            staff = StaffUser.objects.create(user_type=instance)
            staff.save()
        if instance.customer_type == "Seller":
            seller = SellerUser.objects.create(user_type=instance)
            seller.save()
        if instance.customer_type == "Customer":
            customer = CustomerUser.objects.create(user_type=instance)
            customer.save()