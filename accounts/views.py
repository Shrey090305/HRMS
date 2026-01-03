from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .forms import SignUpForm, SignInForm, ProfileUpdateForm
from .models import User
import json


def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employee'  # Default role
            user.save()
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('accounts:signin')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def signin_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to find user by email first, then by username
        user = None
        if '@' in username_or_email:
            # It's an email - use filter().first() to handle duplicates
            user_obj = User.objects.filter(email=username_or_email).first()
            if user_obj:
                user = authenticate(username=user_obj.username, password=password)
        else:
            # It's a username
            user = authenticate(username=username_or_email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('accounts:dashboard_redirect')
        else:
            messages.error(request, 'Invalid email/username or password.')
            
        form = SignInForm()
    else:
        form = SignInForm()
    
    return render(request, 'accounts/signin.html', {'form': form})


@login_required
def signout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:signin')


@login_required
def dashboard_redirect(request):
    """Redirect to appropriate dashboard based on user role"""
    if request.user.is_admin:
        return redirect('employees:admin_dashboard')
    else:
        return redirect('employees:employee_dashboard')


@login_required
def profile_view(request):
    """Display user profile"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def save_salary_view(request):
    """Save salary information for the user"""
    try:
        data = json.loads(request.body)
        
        # Get or create employee profile
        if hasattr(request.user, 'employee_profile'):
            employee = request.user.employee_profile
            
            # Update salary fields
            employee.monthly_wage = float(data.get('monthly_wage', 0))
            employee.yearly_wage = float(data.get('yearly_wage', 0))
            employee.working_days_per_week = int(data.get('working_days_per_week', 5))
            employee.break_time_hours = float(data.get('break_time_hours', 1.0))
            
            # Update calculated components
            employee.basic_salary = float(data.get('basic_salary', 0))
            employee.hra = float(data.get('hra', 0))
            employee.standard_allowance = float(data.get('standard_allowance', 4167.00))
            employee.performance_bonus = float(data.get('performance_bonus', 0))
            employee.lta = float(data.get('lta', 0))
            employee.fixed_allowance = float(data.get('fixed_allowance', 0))
            
            # Update PF contributions
            employee.pf_employee = float(data.get('pf_employee', 0))
            employee.pf_employer = float(data.get('pf_employer', 0))
            
            # Update tax deductions
            employee.professional_tax = float(data.get('professional_tax', 200.00))
            
            employee.save()
            
            return JsonResponse({'success': True, 'message': 'Salary information saved successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Employee profile not found'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
