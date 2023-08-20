from unicodedata import name
from django.db import models

class image(models.Model):
    name = models.CharField(max_length=255)
    base64 = models.TextField()

    def __str__(self):
        return str(self.name)