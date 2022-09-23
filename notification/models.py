import json
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# Create your models here.
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    send_time = models.DateTimeField()
    link = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-send_time']

    def __str__(self):
        return self.title


@receiver(post_save, sender=Notification)
def notification_handel(sender, instance, created, **kwargs):
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.send_time.hour, minute=instance.send_time.minute, day_of_month=instance.send_time.day, month_of_year=instance.send_time.month)
        task = PeriodicTask.objects.create(crontab=schedule, name='notification_'+str(instance.sender.username)+'_'+str(instance.id), task='notification.tasks.notification_send', args =json.dumps([(instance.id)]))
