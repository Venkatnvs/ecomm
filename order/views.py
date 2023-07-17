from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from .models import Order,OrderItems
from store.utilitys import GetCartData
from order.try_img import get_amazon_product_page
from clients.models import Customer

@api_view(['GET','POST'])
def UpdateCartItems(request):
    if request.method == 'POST':
        data = request.data
        productid = data.get("productid",False)
        action = data.get("action",False)
        user = request.user
        if productid and action:
            cust = Customer.objects.filter(user=user).first()
            product = Product.objects.filter(id=productid,is_active=True).first()
            order, created = Order.objects.get_or_create(user=cust,is_completed=False)
            orderitem, created2 = OrderItems.objects.get_or_create(order=order,product=product)
            if action == 'add':
                orderitem.quantity +=1
            if action == 'remove':
                orderitem.quantity -=1
            orderitem.save()
            if orderitem.quantity <= 0:
                orderitem.delete()
    return Response({"message":'updated successfully'})

def try_amas(request):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    context = {
        'items':items,
        'order':order,
    }
    return render(request, 'try/index.html',context)

@api_view(['POST'])
def GetItemsFromAmazon(request):
    data = request.data
    producturl = data.get("producturl",'https://www.amazon.in/gp/product/B0BDJ7P6NG/')
    data = get_amazon_product_page(producturl)
    return Response({"message":data,})
