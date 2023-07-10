from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Product,ProductMedia
from ...utilitys import GetCartData,GetSubAndMainCate

@api_view(['GET','POST'])
def HomeSearch(request):
    rtn_data = []
    data = request.data
    filter_val = data.get("stext",False)
    if filter_val:
        prod = Product.objects.filter(is_active=True,name__istartswith=filter_val)[:6]
        for i in prod:
            img_d = ProductMedia.objects.filter(product=i,is_active=True,type=1).first()
            prod_rt_data = {
                'id':i.pk,
                'name':i.name,
                'slug':i.slug,
                'image':request.build_absolute_uri(img_d.img_url),
            }
            rtn_data.append(prod_rt_data)
        
    return Response({"message":"Query successfully","data":rtn_data})

def SearchResult(request):
    data = request.GET
    squery = data.get("squery",False)
    print(data)
    data = GetCartData(request)
    order = data['order']
    items = data['items']
    product_data = GetProductSearch(request,squery)['product_data']
    catedata = GetSubAndMainCate(request)['categories_list']
    context = {
        'products':product_data,
        'items':items,
        'order':order,
        'categories':catedata,
        'searchdata':squery,
    }
    return render(request, 'search/main.html', context)

def GetProductSearch(request,filter_val):
    product_data = []
    prod = Product.objects.filter(is_active=True,name__istartswith=filter_val)
    for i in prod:
        img_d = ProductMedia.objects.filter(product=i,is_active=True,type=1)
        data = {'product':i,'imgs':img_d}
        product_data.append(data)
    return {'product_data':product_data}