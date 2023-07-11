from store.models import Product,ProductMedia
import numpy as np

def GetProductSearch(request):
    data = request.GET
    squery = data.get("squery",False)
    rpricemin = data.get("rpricemin",0)
    rpricemax = data.get("rpricemax",0)
    discountper = data.get("discountper",0)
    dealsis = data.get("dealsis",False)
    stockava = data.get("stockava",0)
    if stockava=='yes':
        stockava=-999
    elif stockava=='no':
        stockava=0
    else:
        stockava=0
    print(stockava)
    product_data = []
    if rpricemin=="":
        rpricemin=0
    if rpricemax=="":
        rpricemax=np.inf
    if discountper=="":
        discountper=0
    try:
        if rpricemax or rpricemin or discountper:
            prod = Product.objects.filter(
                is_active=True,
                name__istartswith=squery,
                new_price__lte =rpricemax,
                new_price__gte =rpricemin,
                offer__gte = discountper,
                quantity__gte = stockava
            )
        else:
            prod = Product.objects.filter(is_active=True,name__istartswith=squery,quantity__gte = stockava)
    except Exception as e:
        print(e)
        prod = Product.objects.filter(is_active=True,name__istartswith=squery)
    if prod.exists():
        for i in prod:
            img_d = ProductMedia.objects.filter(product=i,is_active=True,type=1)
            data = {'product':i,'imgs':img_d}
            product_data.append(data)
    else:
        return {'product_data':False}
    return {'product_data':product_data}


def GetProCateFilter(request):
    data = request.GET
    squery = data.get("squery",False)
    p_c_filter = []
    if squery:
        prod = Product.objects.filter(is_active=True,name__istartswith=squery)
    else:
        prod = Product.objects.filter(is_active=True,name__istartswith=squery)[0:5]
    if prod.exists():
        for i in prod:
            data = {'subcategory':i.subcategories.name,'category':i.subcategories.category.name}
            p_c_filter.append(data)
    return {'p_c_filter':p_c_filter}