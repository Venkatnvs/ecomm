from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from .models import Order,OrderItems,ShippingAddress,Coupon,BillingAddress
from store.utilitys import GetCartData
from order.try_img import get_amazon_product_page
from clients.models import Customer
from django.http import JsonResponse
import datetime
import json
from clients.models import Customer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.sites.shortcuts import get_current_site
from .models import Order
from io import BytesIO
from django.contrib import messages
from django.conf import settings
import threading
from decouple import config
from django.core.mail import EmailMessage
from django.urls import reverse

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=True)

@api_view(['GET','POST'])
def UpdateCartItems(request):
    if request.method == 'POST':
        data = request.data
        productid = data.get("productid",False)
        action = data.get("action",False)
        user = request.user
        if productid and action:
            cust = Customer.objects.filter(user=user).first()
            product = Product.objects.filter(id=productid,is_active=True,subcategories__category__is_active=True,subcategories__is_active=True).first()
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

def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(user=customer, is_completed=False)
    total = float(data['userFormData']['total'])
    order.transaction_id = transaction_id
    if order.shipping == True:
        billadd,created = BillingAddress.objects.get_or_create(
            user=customer,
            address_1=data['shipping']['address1'],
            address_2=data['shipping']['address2'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
	        )
    else:
        billadd = None
    if total == order.get_cart_total:
        order.is_completed = True
        order.status = "order Confirmed"
        order.payment_type = "Cash on Delivery"
    order.billing = billadd
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
        user=customer,
		order=order,
		address_1=data['shipping']['address1'],
		address_2=data['shipping']['address2'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
	)
    email_tmp_path = 'emails/order/order_successfull.html'
    domain = get_current_site(request).domain
    request_main = config('REQUEST')
    from_mail = config('FROM_MAIL')

    site_url =f"http://{get_current_site(request).domain}"
    context = {
        'order': order,
        'site_name':settings.SITE_NAME,
        "user":request.user,
        "date":datetime.datetime.now,
        "site_url":site_url
        }
    pdf = render_to_pdf('main/orders/invoice_pdf.html', context)
    filename = f'invoice_{order.id}.pdf'

    context_email_data = {
        'title':settings.SITE_NAME,
        'activate_url':f"{request_main}{domain}{reverse('order-generate_invoice_pdf', args=[transaction_id])}",
        'user_name':request.user.username,
        'user_email':request.user.email,
    }
    email = request.user.email
    email_body = get_template(email_tmp_path).render(context_email_data)
    email_subject = f'Order Placed Success | {settings.SITE_NAME}'
    email = EmailMessage(
        email_subject,
        email_body,
        from_mail,
        [email],
    )
    email.content_subtype = 'html'
    email.attach(filename,pdf,'application/pdf')
    EmailThread(email).start()
    messages.success(request, 'Order successfully placed.')
    messages.info(request, 'Invoice is emailed')
    return JsonResponse("processed", safe=False)

@api_view(['GET','POST'])
def GetCouponCode(request):
    data = request.data
    coupon = data.get("coupon",'')
    action = data.get("action",'')
    try:
        details = Coupon.objects.get(code=coupon,is_active=True)
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.get(user=customer,is_completed=False)
        if action == "add":
            if not order.coupon_code.exists():
                order.coupon_code.add(details)
        elif action == "remove":
            if order.coupon_code.exists():
                order.coupon_code.remove(details)
        order.save()
        details = {"code":details.code,"discount":details.discount,"action":action}
        type_d = True
    except Exception as e:
        print(e)
        details = ""
        type_d = False
    return Response({"message":details,"typestatus":type_d})

@api_view(['GET'])
def GetCarBillingTotal(request):
    try:
        customer = Customer.objects.get(user=request.user)
        data_fech = Order.objects.get(user=customer,is_completed=False)
        rtn_data = data_fech.get_cart_billing_total
        type_d = True
    except Exception as e:
        rtn_data = 100000
        type_d = False
    return Response({"message":{"total":rtn_data},"typestatus":type_d})

@api_view(['GET'])
def GetCouponExists(request):
    coupon_st = False
    try:
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.get(user=customer,is_completed=False)
        coupon_st = order.coupon_code.exists()
        if coupon_st:
            coupon = order.coupon_code.first()
            message = {"code":coupon.code,"discount":coupon.discount}
        else:
            message = "no coupon"
        type_d = True
    except Exception as e:
        message = "error"
        type_d = False
    return Response({"message":message,"typestatus":type_d,"coupon_st":coupon_st})

@login_required
def MyOrders(request):
    data_kw = GetCartData(request)
    customer = Customer.objects.get(user=request.user)
    orders_comp = Order.objects.filter(user=customer,is_completed=True,is_delivered=True).order_by('-date')
    orders_pend= Order.objects.filter(user=customer,is_completed=True,is_delivered=False).order_by('-date')
    context = {
        "orders_c":orders_comp,
        "orders_p":orders_pend,
        "order":data_kw['order'],
        "items":data_kw['items']
    }
    return render(request, "main/orders/my_orders.html",context)

@login_required
def order_details(request, order_id):
    data_kw = GetCartData(request)
    order = get_object_or_404(Order, transaction_id=order_id)
    shipping = get_object_or_404(ShippingAddress,order=order)
    context = {
        "orders":order,
        "shipping":shipping,
        "order":data_kw['order'],
        "items":data_kw['items']
    }
    return render(request, 'main/orders/order_details.html',context)

def generate_invoice(request, order_id):
    order = Order.objects.get(transaction_id=order_id)
    
    return render(request, 'main/orders/invoice.html', {'order': order,})

def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None

def generate_invoice_pdf(request, order_id):
    order = Order.objects.get(transaction_id=order_id)
    site_url =f"http://{get_current_site(request).domain}"
    context = {
        'order': order,
        'site_name':settings.SITE_NAME,
        "user":request.user,
        "date":datetime.datetime.now,
        "site_url":site_url
        }
    pdf = render_to_pdf('main/orders/invoice_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'invoice_{order_id}.pdf'
        content = f'inline; filename={filename}'
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF", status=400)