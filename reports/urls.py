from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_dashboard, name='index'),
    path('attendance/', views.attendance_report, name='attendance_report'),
    path('leave/', views.leave_report, name='leave_report'),
    path('payroll/', views.payroll_report, name='payroll_report'),
]
