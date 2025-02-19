from django.urls import path
from . import views

urlpatterns = [
    path('admin_order_list/',views.admin_order_list,name='admin_order_list'),
    path('admin_order_detail/<int:order_id>/',views.admin_order_detail,name='admin_order_detail'),
    path('search_orders_admin/',views.search_orders_admin,name='search_orders_admin'),
    path('cancel_order/<int:item_id>/',views.cancel_order, name='cancel_order'  ),
    path('request_return/<int:item_id>/',views.request_return, name='request_return'  ),
    path('approve_return/<int:item_id>/',views.approve_return, name='approve_return'  ),
                    
]
  