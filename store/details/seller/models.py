from django.db import models
from django.contrib.auth.models import User
from clients.models import SellerUser

class SellerStaff(models.Model):
    customer_type_choices = (
        ("Admin","Admin"),
        ("Manager","Manager"),
        ("Employ","Employ"),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    seller = models.OneToOneField(SellerUser,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Customer/SellerUser/Staff/%Y/%m/%d/')
    customer_type = models.CharField(max_length=100, choices=customer_type_choices, default="Employ")
    is_active = models.BooleanField(default=True)
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
        return f'{self.user.username} ~ {self.customer_type} | {self.seller}'