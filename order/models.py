from django.db import models
from clients.models import Customer
from store.models import Product

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    count = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class BillingAddress(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address_1

class Order(models.Model):
    ORDER_STATUSES = (
        ("Processed","Processed"),
        ("order Confirmed","order Confirmed"),
        ("Shipped","Shipped"),
        ("Out For Delivery","Out For Delivery"),
        ("Delivery","Delivery"),
        ("Cancelled","Cancelled")
    )
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=ORDER_STATUSES, default="Processed")
    ip_address = models.GenericIPAddressField(auto_created=True,null=True,blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    billing = models.ForeignKey(BillingAddress, null=True, on_delete=models.SET_NULL)
    coupon_code = models.ManyToManyField(Coupon,blank=True)
    transaction_id = models.CharField(max_length=255, null=True)
    payment_type = models.CharField(max_length=255,default="COD")
    payment_id = models.CharField(max_length=255,null=True,blank=True)
    payment_status = models.CharField(max_length=255,null=True,blank=True)
    is_delivered = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitems_set.filter(product__is_active=True,product__subcategories__category__is_active=True,product__subcategories__is_active=True)
        for i in orderitems:
            if i.product.is_digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitems_set.filter(product__is_active=True,product__subcategories__category__is_active=True,product__subcategories__is_active=True)
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_item_total(self):
        orderitems = self.orderitems_set.filter(product__is_active=True,product__subcategories__category__is_active=True,product__subcategories__is_active=True)
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_cart_tax(self):
        return (self.get_cart_total * 5) // 100
    
    @property
    def get_cart_shipping(self):
        return 30
    
    @property
    def get_coupon_check(self):
        if self.coupon_code.exists():
            discnt = self.coupon_code.first()
            return discnt
        else:
            return False
        
    @property
    def get_coupon_discount(self):
        if self.coupon_code.exists():
            discnt = self.coupon_code.first()
            discount = discnt.discount
            return discount
        else:
            return None
    
    @property
    def get_cart_billing_total(self):
        total_d = self.get_cart_total + self.get_cart_tax + self.get_cart_shipping
        discount = 0
        if self.coupon_code.exists():
            discnt = self.coupon_code.first()
            discount = discnt.discount
        total_d = total_d - discount
        return total_d

    def __str__(self):
        return f'{self.id}-{self.user}'


class ShippingAddress(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address_1 = models.CharField(max_length=255,null=True,blank=True)
    address_2 = models.CharField(max_length=255,null=True, blank=True)
    state = models.CharField(max_length=255,null=True, blank=True)
    city = models.CharField(max_length=255,null=True, blank=True)
    zipcode = models.CharField(max_length=255,null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.address_1


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00,null=True)
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00,null=True)
    coupon_code = models.CharField(max_length=255,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        total = self.product.new_price * self.quantity
        return total

    def __str__(self):
        return self.product.name