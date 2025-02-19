from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/',views.admin_dash,name='admin_dash'),
    path('sales_report/',views.sales_report,name='sales_report'),
    path('sales-report/download/pdf/', views.generate_pdf_report_view, name='download_pdf_report'),
    path('sales-report/download/excel/', views.generate_excel_report_view, name='download_excel_report'),

]