from django.db import models
from django.contrib.auth import get_user_model
from products.models import product,variant

# Create your models here.
class wishlist(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User,on_delete= models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.id
    
class WhishlistItem(models.Model):
    Wishlist = models.ForeignKey(wishlist, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    variant = models.ForeignKey(variant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='wishlist_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.product.name}"
    
    
    
    

