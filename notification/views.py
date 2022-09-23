from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
from .tasks import test
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta

# Create your views here.
def main(request):
    a = request.GET.get('num')
    test.delay(int(a))
    return HttpResponse('Done')

def note_test(request, message):
    current_time = datetime.now() - timedelta(minutes=5)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notification_'+request.user.username,
        {
            'type':'send_notification',
            'message':{
                'title':'hi',
                'body':message,
                'time': current_time.minute
            }
        }
    )
    return HttpResponse('message:- '+message+' have been sent')
