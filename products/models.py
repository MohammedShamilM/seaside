from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    is_listed = models.BooleanField(default=True)  
    


    def __str__(self):
        return self.name
    
class product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    brand_name = models.CharField(max_length=100)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='products')


    def __str__(self):
        return self.name
    

class variant(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=100,null=True)  
    storage = models.CharField(max_length=100,null=True)  
    RAM = models.CharField(max_length=100,null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_listed = models.BooleanField(default=True)  
    offer = models.IntegerField(null=True,default=0)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.product.name} - {self.color}: {self.storage}"
    
    def save(self, *args, **kwargs):
        

        if not self.offer or int(self.offer) == 0: 
            self.offer_price = None
            
        else:
            self.offer_price = int(float(self.price)) - ((int(float(self.price)) / 100) * int(self.offer))

        if self.offer_price:
            self.final_price = self.offer_price
        else:
            self.final_price = self.price
            

        super().save(*args, **kwargs)       

class VariantImage(models.Model):
    variant = models.ForeignKey(variant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='variant_images/')

    def __str__(self):
        return f"Image for {self.variant.color}"
    

class Review(models.Model):
    product = models.ForeignKey(product,related_name='Rating', on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='Users', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'

    class Meta:
        ordering = ['-created_at']