from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from employees.models import Employee
from .models import Payroll, PayrollComponent
from .forms import PayrollForm, PayrollFilterForm
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
def employee_payroll(request):
    """Employee view for their payroll records"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('employees:employee_dashboard')
    
    filter_form = PayrollFilterForm(request.GET)
    payroll_records = Payroll.objects.filter(employee=employee)
    
    # Apply filters
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('month'):
            payroll_records = payroll_records.filter(month=filter_form.cleaned_data['month'])
        if filter_form.cleaned_data.get('year'):
            payroll_records = payroll_records.filter(year=filter_form.cleaned_data['year'])
        if filter_form.cleaned_data.get('is_paid'):
            is_paid = filter_form.cleaned_data['is_paid'] == 'true'
            payroll_records = payroll_records.filter(is_paid=is_paid)
    
    # Calculate total earnings
    total_earnings = payroll_records.aggregate(total=Sum('net_salary'))['total'] or 0
    
    context = {
        'employee': employee,
        'payroll_records': payroll_records,
        'filter_form': filter_form,
        'total_earnings': total_earnings,
    }
    return render(request, 'payroll/employee_payroll.html', context)


@login_required
def payroll_detail(request, pk):
    """View payroll details"""
    payroll = get_object_or_404(Payroll.objects.select_related('employee__user'), pk=pk)
    
    # Check permissions
    if not request.user.is_admin and payroll.employee.user != request.user:
        messages.error(request, 'You do not have permission to view this payroll.')
        return redirect('payroll:employee_payroll')
    
    # Get components
    components = payroll.components.all()
    
    context = {
        'payroll': payroll,
        'components': components,
    }
    return render(request, 'payroll/payroll_detail.html', context)


@login_required
@admin_required
def admin_payroll(request):
    """Admin view for all payroll records"""
    filter_form = PayrollFilterForm(request.GET)
    payroll_records = Payroll.objects.select_related('employee__user').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        payroll_records = payroll_records.filter(
            Q(employee__employee_id__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query)
        )
    
    # Apply filters
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('month'):
            payroll_records = payroll_records.filter(month=filter_form.cleaned_data['month'])
        if filter_form.cleaned_data.get('year'):
            payroll_records = payroll_records.filter(year=filter_form.cleaned_data['year'])
        if filter_form.cleaned_data.get('is_paid'):
            is_paid = filter_form.cleaned_data['is_paid'] == 'true'
            payroll_records = payroll_records.filter(is_paid=is_paid)
    
    # Calculate totals
    total_payroll = payroll_records.aggregate(total=Sum('net_salary'))['total'] or 0
    
    context = {
        'payroll_records': payroll_records,
        'filter_form': filter_form,
        'search_query': search_query,
        'total_payroll': total_payroll,
    }
    return render(request, 'payroll/admin_payroll.html', context)


@login_required
@admin_required
def add_payroll(request):
    """Add new payroll record"""
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save()
            messages.success(request, 'Payroll record added successfully!')
            return redirect('payroll:payroll_detail', pk=payroll.pk)
    else:
        # Pre-fill with current month/year
        today = date.today()
        form = PayrollForm(initial={'month': today.month, 'year': today.year})
    
    return render(request, 'payroll/add_payroll.html', {'form': form})


@login_required
@admin_required
def edit_payroll(request, pk):
    """Edit payroll record"""
    payroll = get_object_or_404(Payroll, pk=pk)
    
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payroll record updated successfully!')
            return redirect('payroll:payroll_detail', pk=pk)
    else:
        form = PayrollForm(instance=payroll)
    
    return render(request, 'payroll/edit_payroll.html', {'form': form, 'payroll': payroll})


@login_required
@admin_required
def delete_payroll(request, pk):
    """Delete payroll record"""
    payroll = get_object_or_404(Payroll, pk=pk)
    payroll.delete()
    messages.success(request, 'Payroll record deleted successfully!')
    return redirect('payroll:admin_payroll')


@login_required
@admin_required
def mark_paid(request, pk):
    """Mark payroll as paid"""
    payroll = get_object_or_404(Payroll, pk=pk)
    payroll.is_paid = True
    if not payroll.payment_date:
        payroll.payment_date = date.today()
    payroll.save()
    messages.success(request, 'Payroll marked as paid!')
    return redirect('payroll:payroll_detail', pk=pk)
