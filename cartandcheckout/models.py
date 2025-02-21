from django.db import models
from django.contrib.auth import get_user_model
from products.models import product,variant
from decimal import Decimal


# Create your models here.
class cart(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User,on_delete= models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.id

class CartItem(models.Model):
    Cart = models.ForeignKey(cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    variant = models.ForeignKey(variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    image = models.ImageField(upload_to='cart_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.product.name} : {self.quantity}"
    
    
    def get_total_price(self):
        return self.quantity * self.variant.price

    

