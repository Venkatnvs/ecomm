import json
from store.models import Product,ProductMedia,Category,SubCategory
from order.models import Order
from clients.models import Customer

def GetCartData(request):
    if request.user.is_authenticated:
        data = AuthOrderModels(request)
    else:
        data = NoAuthCookies(request)
    return data

def NoAuthCookies(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_item_total':0,'get_cart_total':0}
    for i in cart:
        order['get_item_total'] += cart[i]['quantity']
        product = Product.objects.filter(id=i,is_active=True).first()
        total = product.new_price * cart[i]['quantity']
        img = ProductMedia.objects.filter(product=product,is_active=True,type=1)
        order['get_cart_total'] += total
        item = {
            'product':{
                'id':product.id,
                'name':product.name,
                'new_price':product.new_price,
                'productmedia_set':{
                    'all':img
                }
            },
            'quantity':cart[i]['quantity'],
            'get_total':total
        }
        items.append(item)
    return {'order':order,'items':items}


def AuthOrderModels(request):
    customer = request.user
    cust = Customer.objects.filter(user=customer).first()
    order, created = Order.objects.get_or_create(user=cust,is_completed=False)
    items = order.orderitems_set.all()
    return {'order':order,'items':items}

def GetProductsHome(request):
    product_data = []
    prod = Product.objects.filter(is_active=True)
    for i in prod:
        img_d = ProductMedia.objects.filter(product=i,is_active=True,type=1)
        data = {'product':i,'imgs':img_d}
        product_data.append(data)
    return {'product_data':product_data}

def GetSubAndMainCate(request):
    categories_list = []
    categories = Category.objects.filter(is_active=True)
    for value in categories:
        sub_categories = SubCategory.objects.filter(is_active=True, category=value.id)
        categories_list.append({'category':value, 'subcategory':sub_categories})
    return {
        'categories_list':categories_list,
    }