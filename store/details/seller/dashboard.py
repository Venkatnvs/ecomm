from .models import SellerStaff
from order.models import Order,OrderItems
from store.models import Product

def GetCounts(request,user_to_get):
    cust = SellerStaff.objects.filter(
        seller__user_type__user=user_to_get,
        user__is_active=True
    ).count()

    completed_orders = Order.objects.filter(
        orderitems__product__by_seller__user_type__user=user_to_get,
        is_completed=True
    ).distinct()

    ord_c = completed_orders.filter(is_delivered=True).count()
    ord_n = completed_orders.filter(is_delivered=False).count()

    prod = Product.objects.filter(
        is_active=True,
        subcategories__category__is_active=True,
        subcategories__is_active=True,
        by_seller__user_type__user = user_to_get
    ).count()
    return {"users":cust,"orders_comp":ord_c,"products":prod,"orders_ncomp":ord_n}