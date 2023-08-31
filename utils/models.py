from django.db import models

class ContactUs(models.Model):
    name = models.CharField(default="",max_length=255)
    email = models.EmailField(default="",max_length=255)
    message = models.TextField(default="")
    file = models.FileField(upload_to="main/contacts/uploads/%Y/%m/%d/")
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name - self.created_at}"