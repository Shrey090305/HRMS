from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # Employee routes
    path('', views.employee_payroll, name='employee_payroll'),
    path('<int:pk>/', views.payroll_detail, name='payroll_detail'),
    
    # Admin routes
    path('admin/', views.admin_payroll, name='admin_payroll'),
    path('admin/add/', views.add_payroll, name='add_payroll'),
    path('admin/<int:pk>/edit/', views.edit_payroll, name='edit_payroll'),
    path('admin/<int:pk>/delete/', views.delete_payroll, name='delete_payroll'),
    path('admin/<int:pk>/mark-paid/', views.mark_paid, name='mark_paid'),
]
