from django.db import models

# Create your models here.
class Coupons(models.Model):
    code = models.CharField(max_length=15,unique=True)
    discount = models.IntegerField()
    is_active = models.BooleanField(default=True)
    details = models.CharField(max_length=300)
    expiration_date = models.DateField()
    min_order_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.code