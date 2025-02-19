from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.
class user_address (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.address



