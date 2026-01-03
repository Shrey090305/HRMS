from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # Admin routes
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/list/', views.employee_list, name='employee_list'),
    path('admin/add/', views.add_employee, name='add_employee'),
    path('admin/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('admin/<int:pk>/edit/', views.edit_employee, name='edit_employee'),
    path('admin/<int:pk>/delete/', views.delete_employee, name='delete_employee'),
    
    # Employee routes
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
]
