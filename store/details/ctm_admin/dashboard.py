from clients.models import Customer
from order.models import Order



def GetCounts(request):
    cust = Customer.objects.filter(user__is_active=True).count()
    ord = Order.objects.filter(is_completed=True).count()
    return {"users":cust,"orders":ord}