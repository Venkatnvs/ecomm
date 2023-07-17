from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Product,ProductMedia,Category,SubCategory
from store.utilitys import GetCartData
from .utilitys import GetProductSearch,GetProCateFilter

@api_view(['GET','POST'])
def HomeSearch(request):
    rtn_data = []
    data = request.data
    filter_val = data.get("stext",False)
    if filter_val:
        cate = Category.objects.filter(is_active=True,name__istartswith=filter_val)[:5]
        subcate = SubCategory.objects.filter(is_active=True,name__istartswith=filter_val)[:5]
        prod = Product.objects.filter(is_active=True,name__istartswith=filter_val)[:6]
        for j in cate:
            cate_rt_data = {
                'id':j.pk,
                'name':j.name,
                'slug':j.slug,
                'image':request.build_absolute_uri(j.img_url),
                'type':'cate',
            }
            rtn_data.append(cate_rt_data)
        for k in subcate:
            subcate_rt_data = {
                'id':k.pk,
                'name':k.name,
                'slug':k.slug,
                'image':request.build_absolute_uri(k.img_url),
                'type':'subcate',
            }
            rtn_data.append(subcate_rt_data)
        for i in prod:
            img_d = ProductMedia.objects.filter(product=i,is_active=True,type=1).first()
            prod_rt_data = {
                'id':i.pk,
                'name':i.name,
                'slug':i.slug,
                'image':request.build_absolute_uri(img_d.img_url),
                'type':'prod',
            }
            rtn_data.append(prod_rt_data)
        
    return Response({"message":"Query successfully","data":rtn_data})

def SearchResult(request):
    data = request.GET
    squery = data.get("squery",False)
    data_ct_or = GetCartData(request)
    order = data_ct_or['order']
    items = data_ct_or['items']
    product_data = GetProductSearch(request)['product_data']
    context = {
        'products':product_data,
        'items':items,
        'order':order,
        'searchdata':data,
        'searchcate':GetProCateFilter(request)['p_c_filter']
    }
    return render(request, 'search/main.html', context)
