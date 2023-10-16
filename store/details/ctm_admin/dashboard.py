from clients.models import Customer
from order.models import Order
from store.models import Product
from analytics.models import Visitor
from django.db.models import Count
from django.utils import timezone
import json
from django.core.serializers.json import DjangoJSONEncoder

def GetCounts(request):
    cust = Customer.objects.filter(user__is_active=True).count()
    ord_c = Order.objects.filter(is_completed=True,is_delivered=True).count()
    ord_n = Order.objects.filter(is_completed=True,is_delivered=False).count()
    prod = Product.objects.filter(
        is_active=True,
        subcategories__category__is_active=True,
        subcategories__is_active=True
    ).count()
    return {"users":cust,"orders_comp":ord_c,"products":prod,"orders_ncomp":ord_n}


def unique_visitors_data():
    end_date = timezone.now()  # Current date and time
    start_date = end_date - timezone.timedelta(days=30)  # 30 days ago

    unique_visitors = Visitor.objects.filter(timestamp__date__range=(start_date, end_date)) \
        .values('timestamp__date') \
        .annotate(total=Count('uuid')) \
        .order_by('timestamp__date')

    dates = [entry['timestamp__date'].strftime('%y-%m-%d') for entry in unique_visitors]
    counts = [entry['total'] for entry in unique_visitors]
    return dates, counts

def device_type_data_last_30_days():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=30)

    device_types = Visitor.objects.filter(timestamp__date__range=(start_date, end_date)) \
        .values('devicetype') \
        .annotate(total=Count('uuid'))

    types = [entry['devicetype'] for entry in device_types]
    counts = [entry['total'] for entry in device_types]

    return types, counts