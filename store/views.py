from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import json
from .models import Product,ProductMedia
from .utilitys import GetProductsHome,GetCartData,GetRelatedProducts
from django.contrib.auth.decorators import login_required

def state_dist(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        if search_str == 'Choose...':
            data_a = {'not_state'}
            return JsonResponse(list(data_a), safe=False)
        file_path = os.path.join(settings.BASE_DIR, 'data_files/states_dist.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for v in data:
                x = v['state']
                if x == search_str:
                    data_dist = v['districts']
        data_a = data_dist
        return JsonResponse(list(data_a), safe=False)


def main(request):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    product_data = GetProductsHome(request)['product_data']
    context = {
        'products':product_data,
        'items':items,
        'order':order,
    }
    return render(request, 'main/index.html', context)


def Cart(request):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    context = {
        'items':items,
        'order':order,
        }
    return render(request, 'main/cart.html', context)

@login_required
def Checkout(request):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    states_data = []
    file_path = os.path.join(settings.BASE_DIR, 'data_files/states_dist.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for values in data:
            states_data.append(values['state'])
    context = {
        'data': states_data,
        'items':items,
        'order':order,
    }
    return render(request, 'main/checkout.html', context)

def ProductDetails(request,slug):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    product_data = ''
    prod = Product.objects.filter(slug=slug,is_active=True,subcategories__category__is_active=True,subcategories__is_active=True).first()
    img_d = ProductMedia.objects.filter(product=prod,is_active=True)
    data = {'product':prod,'imgs':img_d}
    product_data = data
    cart_std = True
    try:
        for i in items:
            if request.user.is_authenticated:
                if i.product.id == prod.id:
                    cart_std = False
            else:
                if i["product"]["id"] == prod.id:
                    cart_std = False
    except Exception as e:
        pass
    context = {
        'data':product_data,
        'items':items,
        'order':order,
        'cart_std':cart_std,
        'related_prod':GetRelatedProducts(prod.subcategories.category,prod.id)['product_data']
    }
    return render(request, 'main/productdetails.html', context)