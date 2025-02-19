from django.urls import path
from . import views

urlpatterns = [
   path('userwallet/',views.user_wallet,name= 'wallet'),
                   
]
  