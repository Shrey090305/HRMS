from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    # Employee routes
    path('', views.employee_leave, name='employee_leave'),
    path('apply/', views.apply_leave, name='apply_leave'),
    path('<int:pk>/', views.leave_detail, name='leave_detail'),
    path('<int:pk>/cancel/', views.cancel_leave, name='cancel_leave'),
    
    # Admin routes
    path('admin/', views.admin_leave, name='admin_leave'),
    path('admin/<int:pk>/approve/', views.approve_leave, name='approve_leave'),
    path('update-status/<int:pk>/', views.update_leave_status, name='update_leave_status'),
]
