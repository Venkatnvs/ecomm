from django.db import models
from clients.models import Customer
from store.models import Product

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
    transaction_id = models.CharField(max_length=255, null=True)
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

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

    def __str__(self):
        return str(self.id)


class ShippingAddress(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

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