from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin_dashboard/',views.admin_dash,name='admin_dash'),
    path('admincategories/',views.categories,name='admin_categories'),
    path('addcategory/',views.add_category,name='add_category'),
    path('toggle-category/<int:category_id>/', views.toggle_category_status, name='toggle_category_status'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('adminproducts/',views.products,name='admin_products'),
    path('toggle-product/<int:variant_id>/', views.toggle_product_status, name='toggle_product_status'),
    path('adminproducts-details/<int:variant_id>/',views.products_details,name='admin_products_details'),
    path('addproduct/', views.add_product, name='add_product'),
    path('add-variant/<int:product_id>/', views.add_variant, name='add_variant'),
    path('add-variant-image/<int:variant_id>/', views.add_variant_image, name='add_variant_image'),
    path('edit-product/<int:product_id>/<int:variant_id>/', views.edit_product, name='edit_product'),
    path('edit-variant/<int:variant_id>/', views.edit_variant, name='edit_variant'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  