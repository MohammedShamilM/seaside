from django.urls import path
from . import views

urlpatterns = [
    path('my_account/',views.my_account,name='my_account'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('my_orders/',views.order_list,name='my_orders'),
    path('order_details/<int:order_id>/',views.order_details,name='order_details'),
    path('search/',views.search_orders, name='search_orders'),
    path('my_address/',views.User_address,name='my_address'),
    path('add_address/',views.add_address,name='add_address'),
    path('list_address/<int:address_id>/',views.list_address,name='list_address'),
    path('edit_address/<int:address_id>/',views.edit_address,name='edit_address'),
    path('download_invoice/<int:order_id>/', views.generate_pdf_report_views, name='download_invoice'),

    


]
  