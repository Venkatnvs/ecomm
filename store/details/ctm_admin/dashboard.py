from clients.models import Customer
from order.models import Order
from store.models import Product



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