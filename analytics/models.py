from django.db import models
import uuid
import datetime

class Visitor(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    user = models.CharField(null=True,blank=True,max_length=255)
    count = models.PositiveIntegerField(default=0,null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    duration = models.CharField(max_length=255,blank=True,null=True)
    devicetype = models.CharField(max_length=255,blank=True,null=True)
    useragent = models.TextField(default="",blank=True,null=True)
    ipaddress = models.CharField(max_length=255,null=True,blank=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    is_geolocation = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    city = models.CharField(max_length=255,default=None, null=True,blank=True)
    continent_code = models.CharField(max_length=255,default=None, null=True,blank=True)
    continent_name = models.CharField(max_length=255,default=None, null=True,blank=True)
    country_code = models.CharField(max_length=255,default=None, null=True,blank=True)
    country_name = models.CharField(max_length=255,default=None, null=True,blank=True)
    dma_code = models.CharField(max_length=255,default=None, null=True,blank=True)
    is_in_european_union = models.CharField(max_length=255,default=None, null=True,blank=True)
    postal_code = models.CharField(max_length=255,default=None, null=True,blank=True)
    region = models.CharField(max_length=255,default=None, null=True,blank=True)
    time_zone = models.CharField(max_length=255,default=None, null=True,blank=True)
    latitude = models.FloatField(default=0,blank=True,null=True)
    longitude = models.FloatField(default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} - {self.continent_name}"