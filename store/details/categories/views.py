from django.shortcuts import render
from django.http import HttpResponse
from store.utilitys import GetCartData,GetSubAndMainCate
from store.models import Category,SubCategory,Product,ProductMedia

def CategoriePage(request,slug):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    catedata = GetSubAndMainCate(request)['categories_list']
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
        'categories':catedata,
        'cate_list':categories,
        'products':product_data,
    }
    return render(request,'categories/cate.html',context)

def SubCategoriePage(request,slug):
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    catedata = GetSubAndMainCate(request)['categories_list']
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
        'categories':catedata,
        'subcate_list':subcategories,
        'products':product_data,
    }
    return render(request,'categories/subcate.html',context)