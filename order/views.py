from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from .models import Order,OrderItems

@api_view(['GET','POST'])
def UpdateCartItems(request):
    if request.method == 'POST':
        data = request.data
        productid = data.get("productid",False)
        action = data.get("action",False)
        user = request.user
        if productid and action:
            product = Product.objects.filter(id=productid,is_active=True).first()
            order, created = Order.objects.get_or_create(user__user=user,is_completed=False)
            orderitem, created2 = OrderItems.objects.get_or_create(order=order,product=product)
            if action == 'add':
                orderitem.quantity +=1
            if action == 'remove':
                orderitem.quantity -=1
            orderitem.save()
            if orderitem.quantity <= 0:
                orderitem.delete()
    return Response({"message":'updated successfully'})
