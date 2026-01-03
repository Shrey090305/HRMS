from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Employee routes
    path('', views.employee_attendance, name='employee_attendance'),
    path('mark/', views.mark_attendance_ajax, name='mark_attendance_ajax'),
    path('status/', views.attendance_status, name='attendance_status'),
    
    # Admin routes
    path('admin/', views.admin_attendance, name='admin_attendance'),
    path('admin/mark/<int:employee_id>/', views.mark_attendance, name='mark_attendance'),
    path('admin/edit/<int:pk>/', views.edit_attendance, name='edit_attendance'),
    path('admin/delete/<int:pk>/', views.delete_attendance, name='delete_attendance'),
]
