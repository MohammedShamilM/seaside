from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Wallet(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, default=0.00,max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.balance

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=30)
    amount = models.DecimalField(decimal_places=2, default=0.00,max_digits=10)
    balance_after = models.DecimalField(decimal_places=2, default=0.00,max_digits=10)
    details = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)