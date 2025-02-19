# base/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
import random
from datetime import timedelta
from django.utils import timezone

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    

class OTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def generate_otp(cls, user):
        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        expires_at = timezone.now() + timedelta(minutes=5)  # OTP expires after 5 minutes
        otp_instance = cls.objects.create(
            user=user,
            otp=str(otp),
            expires_at=expires_at
        )
        return otp_instance