from django.shortcuts import render
from django.http import HttpResponse
from store.utilitys import GetCartData
from store.models import Category,SubCategory,Product,ProductMedia

def CategoriePage(request,slug):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    categories = Category.objects.filter(slug=slug,is_active=True).first()
    product_data = []
    prod = Product.objects.filter(is_active=True,subcategories__category = categories)
    for i in prod:
        img_d = ProductMedia.objects.filter(product=i,is_active=True,type=1)
        data = {'product':i,'imgs':img_d}
        product_data.append(data)
    context = {
        'items':items,
        'order':order,
        'cate_list':categories,
        'products':product_data,
    }
    return render(request,'categories/cate.html',context)

def SubCategoriePage(request,slug):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    subcategories = SubCategory.objects.filter(slug=slug,is_active=True).first()
    product_data = []
    prod = Product.objects.filter(is_active=True,subcategories=subcategories)
    for i in prod:
        img_d = ProductMedia.objects.filter(product=i,is_active=True,type=1)
        data = {'product':i,'imgs':img_d}
        product_data.append(data)
    context = {
        'items':items,
        'order':order,
        'subcate_list':subcategories,
        'products':product_data,
    }
    return render(request,'categories/subcate.html',context)