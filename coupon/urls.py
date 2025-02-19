from django.urls import path
from . import views

urlpatterns = [
    path('coupons/', views.coupon, name='coupons'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('toggle-coupon-status/<int:coupon_id>/', views.toggle_coupon_status, name='toggle-coupon-status'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('coupon_apply/', views.apply_coupon, name='apply_coupon'),
]


