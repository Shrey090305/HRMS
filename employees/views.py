from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from accounts.models import User
from .models import Employee
from .forms import EmployeeCreationForm, EmployeeUpdateForm
from attendance.models import Attendance
from leave.models import LeaveRequest
from datetime import date


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
def admin_dashboard(request):
    """Admin dashboard with employee cards"""
    total_employees = Employee.objects.filter(is_active=True).count()
    total_users = User.objects.filter(is_active=True).count()
    
    # Today's attendance
    today = date.today()
    today_attendance = Attendance.objects.filter(date=today).count()
    
    # Pending leave requests
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    
    # Get all employees
    employees = Employee.objects.filter(is_active=True).select_related('user')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            Q(employee_id__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    
    # Get today's attendance records
    attendance_today = {a.employee_id: a for a in Attendance.objects.filter(date=today).select_related('employee')}
    
    # Get approved leaves for today
    leaves_today = LeaveRequest.objects.filter(
        status='approved',
        start_date__lte=today,
        end_date__gte=today
    ).select_related('employee')
    leave_employee_ids = {leave.employee_id for leave in leaves_today}
    
    # Add status to each employee
    employees_list = list(employees)
    for emp in employees_list:
        if emp.id in leave_employee_ids:
            emp.status = 'on_leave'
        elif emp.id in attendance_today:
            # Use the actual attendance status from the database
            emp.status = attendance_today[emp.id].status
        else:
            emp.status = 'absent'
    
    context = {
        'total_employees': total_employees,
        'total_users': total_users,
        'today_attendance': today_attendance,
        'pending_leaves': pending_leaves,
        'employees': employees_list,
        'search_query': search_query,
    }
    return render(request, 'employees/admin_dashboard.html', context)


@login_required
def employee_dashboard(request):
    """Employee dashboard with all employees list"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.warning(request, 'Your employee profile is not set up yet. Please contact HR.')
        employee = None
    
    # Get all active employees
    employees = Employee.objects.filter(is_active=True).select_related('user')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            Q(employee_id__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    
    # Statistics for header
    today = date.today()
    total_employees = Employee.objects.filter(is_active=True).count()
    today_attendance = Attendance.objects.filter(date=today).count()
    
    # Get today's attendance records
    attendance_today = {a.employee_id: a for a in Attendance.objects.filter(date=today).select_related('employee')}
    
    # Get approved leaves for today
    leaves_today = LeaveRequest.objects.filter(
        status='approved',
        start_date__lte=today,
        end_date__gte=today
    ).select_related('employee')
    leave_employee_ids = {leave.employee_id for leave in leaves_today}
    
    # Add status to each employee
    employees_list = list(employees)
    for emp in employees_list:
        if emp.id in leave_employee_ids:
            emp.status = 'on_leave'
        elif emp.id in attendance_today:
            # Use the actual attendance status from the database
            emp.status = attendance_today[emp.id].status
        else:
            emp.status = 'absent'
    
    context = {
        'employee': employee,
        'employees': employees_list,
        'search_query': search_query,
        'total_employees': total_employees,
        'today_attendance': today_attendance,
    }
    return render(request, 'employees/employee_dashboard.html', context)


@login_required
@admin_required
def employee_list(request):
    """List all employees"""
    employees = Employee.objects.select_related('user').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            Q(employee_id__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    
    context = {'employees': employees, 'search_query': search_query}
    return render(request, 'employees/employee_list.html', context)


@login_required
@admin_required
def add_employee(request):
    """Add new employee"""
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            employee = form.save()
            # Show the generated credentials
            messages.success(request, f'Employee added successfully! Login ID: {employee.generated_username}, Password: {employee.generated_password}')
            return redirect('employees:employee_list')
    else:
        form = EmployeeCreationForm()
    
    return render(request, 'employees/add_employee.html', {'form': form})


@login_required
@admin_required
def edit_employee(request, pk):
    """Edit employee information"""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employees:employee_detail', pk=pk)
    else:
        form = EmployeeUpdateForm(instance=employee)
    
    return render(request, 'employees/edit_employee.html', {'form': form, 'employee': employee})


@login_required
@admin_required
def employee_detail(request, pk):
    """View employee details"""
    employee = get_object_or_404(Employee.objects.select_related('user'), pk=pk)
    
    # Get attendance summary
    attendance_count = Attendance.objects.filter(employee=employee).count()
    
    # Get leave summary
    leave_count = LeaveRequest.objects.filter(employee=employee).count()
    
    context = {
        'employee': employee,
        'attendance_count': attendance_count,
        'leave_count': leave_count,
    }
    return render(request, 'employees/employee_detail.html', context)


@login_required
@admin_required
def delete_employee(request, pk):
    """Soft delete employee (deactivate)"""
    employee = get_object_or_404(Employee, pk=pk)
    employee.is_active = False
    employee.user.is_active = False
    employee.save()
    employee.user.save()
    messages.success(request, 'Employee deactivated successfully!')
    return redirect('employees:employee_list')
