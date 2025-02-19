from django.urls import path
from . import views


urlpatterns = [
    
    path('home/',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('product_details/<int:product_id>/',views.product_details,name='products_details'),
    path('admin_search/', views.search_product, name='search_product'),
    path('sort/',views.product_sort, name='product_sort'),
   

] 
  