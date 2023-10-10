from django.shortcuts import render
from store.utilitys import GetCartData

def MainProfile(request):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    context = {
        'items':items,
        'order':order,
    }
    return render(request,"account/index.html",context)