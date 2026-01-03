from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from employees.models import Employee
from .models import LeaveRequest, LeaveAllocation
from .forms import LeaveRequestForm, LeaveApprovalForm, LeaveFilterForm
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
def employee_leave(request):
    """Employee view for their leave requests"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('employees:employee_dashboard')
    
    filter_form = LeaveFilterForm(request.GET)
    leave_requests = LeaveRequest.objects.filter(employee=employee)
    
    # Apply filters
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('leave_type'):
            leave_requests = leave_requests.filter(leave_type=filter_form.cleaned_data['leave_type'])
        if filter_form.cleaned_data.get('status'):
            leave_requests = leave_requests.filter(status=filter_form.cleaned_data['status'])
        if filter_form.cleaned_data.get('start_date'):
            leave_requests = leave_requests.filter(start_date__gte=filter_form.cleaned_data['start_date'])
        if filter_form.cleaned_data.get('end_date'):
            leave_requests = leave_requests.filter(end_date__lte=filter_form.cleaned_data['end_date'])
    
    # Get or create allocation for employee
    allocation, created = LeaveAllocation.objects.get_or_create(employee=employee)
    
    context = {
        'employee': employee,
        'leave_requests': leave_requests,
        'filter_form': filter_form,
        'allocation': allocation,
    }
    return render(request, 'leave/employee_leave.html', context)


@login_required
def apply_leave(request):
    """Apply for leave"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('employees:employee_dashboard')
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = employee
            leave_request.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('leave:employee_leave')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'leave/apply_leave.html', {'form': form})


@login_required
def leave_detail(request, pk):
    """View leave request details"""
    leave_request = get_object_or_404(LeaveRequest.objects.select_related('employee__user'), pk=pk)
    
    # Check permissions
    if not request.user.is_admin and leave_request.employee.user != request.user:
        messages.error(request, 'You do not have permission to view this leave request.')
        return redirect('leave:employee_leave')
    
    return render(request, 'leave/leave_detail.html', {'leave_request': leave_request})


@login_required
@admin_required
def admin_leave(request):
    """Admin view for all leave requests"""
    filter_form = LeaveFilterForm(request.GET)
    leave_requests = LeaveRequest.objects.select_related('employee__user').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        leave_requests = leave_requests.filter(
            Q(employee__employee_id__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query)
        )
    
    # Apply filters
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('leave_type'):
            leave_requests = leave_requests.filter(leave_type=filter_form.cleaned_data['leave_type'])
        if filter_form.cleaned_data.get('status'):
            leave_requests = leave_requests.filter(status=filter_form.cleaned_data['status'])
        if filter_form.cleaned_data.get('start_date'):
            leave_requests = leave_requests.filter(start_date__gte=filter_form.cleaned_data['start_date'])
        if filter_form.cleaned_data.get('end_date'):
            leave_requests = leave_requests.filter(end_date__lte=filter_form.cleaned_data['end_date'])
    
    # Get or create allocation for current user (admin)
    allocation = None
    if hasattr(request.user, 'employee_profile'):
        allocation, created = LeaveAllocation.objects.get_or_create(
            employee=request.user.employee_profile
        )
    
    context = {
        'leave_requests': leave_requests,
        'filter_form': filter_form,
        'search_query': search_query,
        'allocation': allocation,
    }
    return render(request, 'leave/admin_leave.html', context)


@login_required
@admin_required
@require_http_methods(["POST"])
def update_leave_status(request, pk):
    """Update leave request status via AJAX"""
    try:
        leave_request = get_object_or_404(LeaveRequest, pk=pk)
        data = json.loads(request.body)
        status = data.get('status')
        
        if status not in ['approved', 'rejected']:
            return JsonResponse({'success': False, 'message': 'Invalid status'})
        
        leave_request.status = status
        if hasattr(request.user, 'employee_profile'):
            leave_request.approved_by = request.user.employee_profile
        leave_request.save()
        
        return JsonResponse({'success': True, 'message': f'Leave request {status} successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@admin_required
def approve_leave(request, pk):
    """Approve or reject leave request"""
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave = form.save(commit=False)
            if request.user.employee_profile:
                leave.approved_by = request.user.employee_profile
            leave.save()
            
            status_msg = 'approved' if leave.status == 'approved' else 'rejected'
            messages.success(request, f'Leave request {status_msg} successfully!')
            return redirect('leave:admin_leave')
    else:
        form = LeaveApprovalForm(instance=leave_request)
    
    return render(request, 'leave/approve_leave.html', {'form': form, 'leave_request': leave_request})


@login_required
def cancel_leave(request, pk):
    """Cancel leave request (employee only, if pending)"""
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    # Check permissions
    if leave_request.employee.user != request.user:
        messages.error(request, 'You do not have permission to cancel this leave request.')
        return redirect('leave:employee_leave')
    
    if leave_request.status != 'pending':
        messages.error(request, 'You can only cancel pending leave requests.')
        return redirect('leave:employee_leave')
    
    leave_request.delete()
    messages.success(request, 'Leave request cancelled successfully!')
    return redirect('leave:employee_leave')
