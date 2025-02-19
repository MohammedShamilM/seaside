from django.urls import path
from . import views

urlpatterns = [
    path('user-list/',views.user_list,name='user_list'),
    path('toggle-product-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),


]
  