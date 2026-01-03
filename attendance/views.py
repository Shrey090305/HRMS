from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import date, datetime
import json
from employees.models import Employee
from .models import Attendance
from .forms import AttendanceForm, AttendanceFilterForm


def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:signin')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def employee_attendance(request):
    """Employee view for marking their own attendance"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('employees:employee_dashboard')
    
    from datetime import timedelta
    from calendar import monthrange
    
    # Get the selected date from URL parameter or default to today
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # Calculate month boundaries
    month_start = selected_date.replace(day=1)
    last_day = monthrange(selected_date.year, selected_date.month)[1]
    month_end = selected_date.replace(day=last_day)
    
    # Calculate previous and next month dates
    if selected_date.month == 1:
        prev_month = selected_date.replace(year=selected_date.year - 1, month=12, day=1)
    else:
        prev_month = selected_date.replace(month=selected_date.month - 1, day=1)
    
    if selected_date.month == 12:
        next_month = selected_date.replace(year=selected_date.year + 1, month=1, day=1)
    else:
        next_month = selected_date.replace(month=selected_date.month + 1, day=1)
    
    # Get attendance records for the month
    attendance_records = Attendance.objects.filter(
        employee=employee,
        date__gte=month_start,
        date__lte=month_end
    ).order_by('date')
    
    # Calculate statistics
    days_present = attendance_records.filter(status='present').count()
    
    # Count leave days
    from leave.models import LeaveRequest
    leaves_count = LeaveRequest.objects.filter(
        employee=employee,
        status='approved',
        start_date__lte=month_end,
        end_date__gte=month_start
    ).count()
    
    # Total working days in month (excluding Sundays)
    total_working_days = 0
    current_date = month_start
    while current_date <= month_end:
        if current_date.weekday() != 6:  # 6 = Sunday
            total_working_days += 1
        current_date += timedelta(days=1)
    
    # Format month name
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_month_name = month_names[selected_date.month - 1]
    
    context = {
        'employee': employee,
        'attendance_records': attendance_records,
        'days_present': days_present,
        'leaves_count': leaves_count,
        'total_working_days': total_working_days,
        'current_month_name': current_month_name,
        'current_year': selected_date.year,
        'current_month': f"{selected_date.month:02d}",
        'current_date_display': selected_date.strftime('%d,%B %Y'),
        'prev_month': prev_month.strftime('%Y-%m-%d'),
        'next_month': next_month.strftime('%Y-%m-%d'),
    }
    return render(request, 'attendance/employee_attendance.html', context)


@login_required
@admin_required
def admin_attendance(request):
    """Admin view for managing all attendance records"""
    from datetime import timedelta
    
    # Get the selected date (default to today)
    date_str = request.GET.get('date', '')
    if date_str:
        try:
            current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            current_date = date.today()
    else:
        current_date = date.today()
    
    # Calculate previous and next dates
    prev_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)
    
    # Get view type (day, week, month)
    view_type = request.GET.get('view', 'day')
    
    # Get attendance records based on view type
    if view_type == 'day':
        # Show all employees present on the selected day
        attendance_records = Attendance.objects.filter(
            date=current_date,
            status='present'
        ).select_related('employee__user').order_by('employee__user__first_name')
    elif view_type == 'week':
        # Show week view
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)
        attendance_records = Attendance.objects.filter(
            date__gte=week_start,
            date__lte=week_end
        ).select_related('employee__user').order_by('-date', 'employee__user__first_name')
    elif view_type == 'month':
        # Show month view
        attendance_records = Attendance.objects.filter(
            date__year=current_date.year,
            date__month=current_date.month
        ).select_related('employee__user').order_by('-date', 'employee__user__first_name')
    else:
        attendance_records = Attendance.objects.filter(
            date=current_date
        ).select_related('employee__user').order_by('employee__user__first_name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        attendance_records = attendance_records.filter(
            Q(employee__employee_id__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query)
        )
    
    context = {
        'attendance_records': attendance_records,
        'search_query': search_query,
        'current_date': current_date,
        'prev_date': prev_date.strftime('%Y-%m-%d'),
        'next_date': next_date.strftime('%Y-%m-%d'),
        'view_type': view_type,
    }
    return render(request, 'attendance/admin_attendance.html', context)


@login_required
@admin_required
def mark_attendance(request, employee_id):
    """Admin mark attendance for an employee"""
    employee = get_object_or_404(Employee, pk=employee_id)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.employee = employee
            attendance.save()
            messages.success(request, 'Attendance marked successfully!')
            return redirect('attendance:admin_attendance')
    else:
        form = AttendanceForm(initial={'date': date.today()})
    
    return render(request, 'attendance/mark_attendance.html', {'form': form, 'employee': employee})


@login_required
@admin_required
def edit_attendance(request, pk):
    """Edit attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance updated successfully!')
            return redirect('attendance:admin_attendance')
    else:
        form = AttendanceForm(instance=attendance)
    
    return render(request, 'attendance/edit_attendance.html', {'form': form, 'attendance': attendance})


@login_required
@admin_required
def delete_attendance(request, pk):
    """Delete attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.delete()
    messages.success(request, 'Attendance record deleted successfully!')
    return redirect('attendance:admin_attendance')


@login_required
@require_http_methods(["POST"])
def mark_attendance_ajax(request):
    """AJAX endpoint for marking attendance from navbar"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Employee profile not found'})
    
    data = json.loads(request.body)
    action = data.get('action')
    today = date.today()
    
    # Get or create today's attendance
    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today,
        defaults={'status': 'absent'}
    )
    
    if action == 'check_in':
        # Only show error if trying to check in when already checked in AND not checked out
        if attendance.check_in_time and not attendance.check_out_time:
            return JsonResponse({
                'success': False,
                'message': 'Already checked in'
            })
        # Allow checking in again after checkout or first time
        attendance.check_in_time = datetime.now().time()
        attendance.check_out_time = None  # Reset checkout time
        attendance.status = 'present'
        attendance.save()
        return JsonResponse({
            'success': True,
            'message': f'Checked in at {attendance.check_in_time.strftime("%I:%M %p")}'
        })
    
    elif action == 'check_out':
        # Only show error if trying to checkout when already checked out
        if attendance.check_out_time and attendance.check_in_time:
            return JsonResponse({
                'success': False,
                'message': 'Already checked out'
            })
        # Must check in first
        if not attendance.check_in_time:
            return JsonResponse({
                'success': False,
                'message': 'Please check in first'
            })
        attendance.check_out_time = datetime.now().time()
        attendance.save()
        return JsonResponse({
            'success': True,
            'message': f'Checked out at {attendance.check_out_time.strftime("%I:%M %p")}'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid action'})


@login_required
def attendance_status(request):
    """Get current attendance status for navbar marker"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        return JsonResponse({'checked_in': False, 'checked_out': False})
    
    today = date.today()
    attendance = Attendance.objects.filter(employee=employee, date=today).first()
    
    if attendance:
        return JsonResponse({
            'checked_in': bool(attendance.check_in_time),
            'checked_out': bool(attendance.check_out_time)
        })
    
    return JsonResponse({'checked_in': False, 'checked_out': False})
