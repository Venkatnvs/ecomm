import asyncio
from celery import shared_task
from channels.layers import get_channel_layer
from .models import Notification
from celery import Celery, states
from celery.exceptions import Ignore
from .fun import fun

@shared_task(bind=True)
def test(self, v):
    fun(v)
    return 'Done1'

@shared_task(bind=True)
def notification_send(self, data):
    print('data:- '+str(data))
    # print('v:- '+v)
    try:
        notification = Notification.objects.filter(id=data)
        if notification.exists():
            # print(self.request.user.username)
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                'notification_venkat',
                {
                    'type':'send_notification',
                    'message':{
                        'title':notification.title,
                        'body':notification.message,
                        'time':notification.created_at.minute
                    }
                }
            ))
            notification.sent = True
            notification.save()
            return 'Done'
        else:
            print('not found')
            self.update_state(
            state = 'FAILURE',
            meta = {
                'exe':'message not found'
            }
        )
        raise Ignore()
    except Exception as e:
        print('try')
        print(e)
        self.update_state(
            state = 'FAILURE',
            meta = {
                'exe':'message not found'
            }
        )
        raise Ignore()