from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('blog-detail', args=(str(self.id)))