from django.urls import path
from . import views

urlpatterns = [
    path('cart/',views.Cart,name='cart'),
    path('add-to-cart/<int:variant_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<int:variant_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('add_quantity/<int:variant_id>/',views.add_quantity,name='add_quantity'),
    path('remove_quantity/<int:variant_id>/',views.remove_quantity,name='remove_quantity'),
    path('checkout/',views.checkout,name='checkout'),
    path('orderPlaced/',views.orderPlaced,name='orderplaced'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('update-cart/', views.update_cart, name='update_cart'),
    



]
  