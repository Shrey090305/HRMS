from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from django.db.models.functions import TruncMonth
from datetime import date, datetime, timedelta
from employees.models import Employee
from attendance.models import Attendance
from leave.models import LeaveRequest
from payroll.models import Payroll
import json


def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:signin')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def reports_dashboard(request):
    """Main reports dashboard with overview"""
    # Current stats
    total_employees = Employee.objects.filter(is_active=True).count()
    today = date.today()
    
    # Attendance stats
    today_attendance = Attendance.objects.filter(date=today).count()
    attendance_rate = (today_attendance / total_employees * 100) if total_employees > 0 else 0
    
    # Leave stats
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    approved_leaves = LeaveRequest.objects.filter(status='approved').count()
    
    # Payroll stats
    current_month = today.month
    current_year = today.year
    monthly_payroll = Payroll.objects.filter(
        month=current_month, 
        year=current_year
    ).aggregate(total=Sum('net_salary'))['total'] or 0
    
    # Department distribution
    dept_distribution = Employee.objects.filter(is_active=True).values('department').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'total_employees': total_employees,
        'today_attendance': today_attendance,
        'attendance_rate': round(attendance_rate, 2),
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'monthly_payroll': monthly_payroll,
        'dept_distribution': dept_distribution,
    }
    return render(request, 'reports/index.html', context)


@login_required
@admin_required
def attendance_report(request):
    """Detailed attendance report"""
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    department = request.GET.get('department')
    
    # Default to current month if no filters
    if not start_date or not end_date:
        today = date.today()
        start_date = date(today.year, today.month, 1).isoformat()
        end_date = today.isoformat()
    
    # Query attendance
    attendance_records = Attendance.objects.filter(
        date__range=[start_date, end_date]
    ).select_related('employee__user')
    
    if department:
        attendance_records = attendance_records.filter(employee__department=department)
    
    # Aggregate by employee
    employee_attendance = {}
    for record in attendance_records:
        emp_id = record.employee.id
        if emp_id not in employee_attendance:
            employee_attendance[emp_id] = {
                'employee': record.employee,
                'present': 0,
                'absent': 0,
                'half_day': 0,
                'on_leave': 0,
                'total_hours': 0,
            }
        
        if record.status == 'present':
            employee_attendance[emp_id]['present'] += 1
        elif record.status == 'absent':
            employee_attendance[emp_id]['absent'] += 1
        elif record.status == 'half-day':
            employee_attendance[emp_id]['half_day'] += 1
        elif record.status == 'on-leave':
            employee_attendance[emp_id]['on_leave'] += 1
        
        employee_attendance[emp_id]['total_hours'] += record.working_hours
    
    # Status distribution
    status_distribution = attendance_records.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Get all departments for filter
    departments = Employee.objects.values_list('department', flat=True).distinct()
    
    context = {
        'employee_attendance': employee_attendance.values(),
        'status_distribution': status_distribution,
        'start_date': start_date,
        'end_date': end_date,
        'department': department,
        'departments': departments,
    }
    return render(request, 'reports/attendance_report.html', context)


@login_required
@admin_required
def leave_report(request):
    """Detailed leave report"""
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    leave_type = request.GET.get('leave_type')
    status = request.GET.get('status')
    
    # Default to current year if no filters
    if not start_date or not end_date:
        today = date.today()
        start_date = date(today.year, 1, 1).isoformat()
        end_date = today.isoformat()
    
    # Query leave requests
    leave_requests = LeaveRequest.objects.filter(
        start_date__range=[start_date, end_date]
    ).select_related('employee__user')
    
    if leave_type:
        leave_requests = leave_requests.filter(leave_type=leave_type)
    if status:
        leave_requests = leave_requests.filter(status=status)
    
    # Aggregate by employee
    employee_leaves = {}
    for leave in leave_requests:
        emp_id = leave.employee.id
        if emp_id not in employee_leaves:
            employee_leaves[emp_id] = {
                'employee': leave.employee,
                'total_days': 0,
                'approved': 0,
                'pending': 0,
                'rejected': 0,
            }
        
        employee_leaves[emp_id]['total_days'] += leave.duration_days
        
        if leave.status == 'approved':
            employee_leaves[emp_id]['approved'] += 1
        elif leave.status == 'pending':
            employee_leaves[emp_id]['pending'] += 1
        elif leave.status == 'rejected':
            employee_leaves[emp_id]['rejected'] += 1
    
    # Leave type distribution
    type_distribution = leave_requests.values('leave_type').annotate(
        count=Count('id')
    ).order_by('leave_type')
    
    # Status distribution
    status_distribution = leave_requests.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    context = {
        'employee_leaves': employee_leaves.values(),
        'type_distribution': type_distribution,
        'status_distribution': status_distribution,
        'start_date': start_date,
        'end_date': end_date,
        'leave_type': leave_type,
        'status': status,
        'leave_types': LeaveRequest.LEAVE_TYPE_CHOICES,
        'statuses': LeaveRequest.STATUS_CHOICES,
    }
    return render(request, 'reports/leave_report.html', context)


@login_required
@admin_required
def payroll_report(request):
    """Detailed payroll report"""
    # Get filter parameters
    year = request.GET.get('year', date.today().year)
    department = request.GET.get('department')
    
    # Query payroll
    payroll_records = Payroll.objects.filter(year=year).select_related('employee__user')
    
    if department:
        payroll_records = payroll_records.filter(employee__department=department)
    
    # Monthly totals
    monthly_totals = payroll_records.values('month').annotate(
        total=Sum('net_salary'),
        count=Count('id')
    ).order_by('month')
    
    # Department-wise distribution
    dept_payroll = payroll_records.values('employee__department').annotate(
        total=Sum('net_salary'),
        count=Count('id')
    ).order_by('-total')
    
    # Total payroll
    total_payroll = payroll_records.aggregate(total=Sum('net_salary'))['total'] or 0
    
    # Get all departments for filter
    departments = Employee.objects.values_list('department', flat=True).distinct()
    
    context = {
        'monthly_totals': monthly_totals,
        'dept_payroll': dept_payroll,
        'total_payroll': total_payroll,
        'year': year,
        'department': department,
        'departments': departments,
    }
    return render(request, 'reports/payroll_report.html', context)
