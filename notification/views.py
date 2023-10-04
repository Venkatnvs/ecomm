from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
from .tasks import test
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
def main(request):
    a = request.GET.get('num',5)
    test.delay(int(a))
    return HttpResponse('Done')

def note_test_all(title , message):
    current_time = datetime.now()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notification_nvstrades',
        {
            'type':'send_notification',
            'message':{
                'title':title,
                'body':message,
                'time': "now"
            }
        }
    )
    return True

@login_required
@user_passes_test(lambda u: u.is_superuser)
def SendNotificationAll(request):
    if request.method == 'GET':
        return render(request,"ctm_admin/notification.html")
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        a = note_test_all(title,content)
        if a:
            messages.success(request, 'Notification Send!..')
        return render(request,"ctm_admin/notification.html")