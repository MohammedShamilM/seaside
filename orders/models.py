from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta  
from django.utils import timezone 
from products.models import product,variant


User = get_user_model()

class shipping_address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_address')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.address


# Create your models here.
class orders(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('RazorPay', 'Razor Pay'),
        ('Wallet', 'Wallet')
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failure', 'Failure'),
        ('Refunded', 'Refunded')
    ]
    STATUS_CHOICES = [
        ("Order Pending", "Order Pending"),
        ("Order confirmed", "Order confirmed"),
        ("Shipped", "Shipped"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Returned", "Returned")

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    order_id = models.CharField(max_length=6,unique=True,editable=False)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    discount = models.IntegerField(null=True)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    order_status = models.CharField(max_length=30,choices=STATUS_CHOICES,default='Order Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=50,choices=PAYMENT_STATUS_CHOICES, default='Pending')
    shipping_address = models.ForeignKey(shipping_address,on_delete=models.CASCADE)
    shipping_fees = models.IntegerField(null=True)
    estimated_delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'Order by {self.user.username}'
    
    def save(self, *args, **kwargs):
        

        if not self.estimated_delivery_date:
            self.estimated_delivery_date = timezone.now().date() + timedelta(days=3)

        super().save(*args, **kwargs)







    
class order_items(models.Model):
    STATUS_CHOICES = [
        ("Order Pending", "Order Pending"),
        ("Order confirmed", "Order confirmed"),
        ("Shipped", "Shipped"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Requested Return", "Requested Return"),
        ("Approve Return", "Approve Return"),
        ("Returned", "Returned")
    ]
    
    order = models.ForeignKey(orders,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    variant = models.ForeignKey(variant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Order Pending') 
    price = models.DecimalField(max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product

