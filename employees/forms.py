from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from .models import Employee
import random
import string
from datetime import datetime


class EmployeeCreationForm(forms.ModelForm):
    """Form for creating a new employee (admin use)"""
    company_name = forms.CharField(max_length=100, initial='Odoo India', help_text='Company Name')
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required=False)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = Employee
        fields = ['employee_id', 'department', 'designation', 'employment_type', 
                  'date_of_joining', 'salary', 'manager', 'emergency_contact_name', 
                  'emergency_contact_number']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
    
    def generate_username(self, first_name, last_name, year_of_joining):
        """Generate username in format: OI[FirstName2][LastName2][Year][Serial]"""
        # Get company initials (OI for Odoo India)
        company_initials = 'OI'
        
        # Get first 2 letters of first and last name
        first_two = first_name[:2].upper() if len(first_name) >= 2 else first_name.upper().ljust(2, 'X')
        last_two = last_name[:2].upper() if len(last_name) >= 2 else last_name.upper().ljust(2, 'X')
        
        # Get year
        year = str(year_of_joining)
        
        # Get serial number for this year
        year_start = datetime(year_of_joining, 1, 1).date()
        year_end = datetime(year_of_joining, 12, 31).date()
        
        count = Employee.objects.filter(
            date_of_joining__gte=year_start,
            date_of_joining__lte=year_end
        ).count() + 1
        
        serial = str(count).zfill(4)
        
        username = f"{company_initials}{first_two}{last_two}{year}{serial}"
        return username
    
    def generate_password(self, length=10):
        """Generate a random password"""
        characters = string.ascii_letters + string.digits + "!@#$%"
        password = ''.join(random.choice(characters) for i in range(length))
        return password
    
    def save(self, commit=True):
        # Get employee data
        employee = super().save(commit=False)
        
        # Generate username and password
        year_of_joining = employee.date_of_joining.year
        username = self.generate_username(
            self.cleaned_data['first_name'],
            self.cleaned_data['last_name'],
            year_of_joining
        )
        password = self.generate_password()
        
        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role='employee'
        )
        
        # Link user to employee
        employee.user = user
        
        if commit:
            employee.save()
        
        # Store password in session or send via email (for now, store in a temp attribute)
        employee.generated_password = password
        employee.generated_username = username
        
        return employee


class EmployeeUpdateForm(forms.ModelForm):
    """Form for updating employee information"""
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    class Meta:
        model = Employee
        fields = ['department', 'designation', 'employment_type', 'salary', 
                  'manager', 'emergency_contact_name', 'emergency_contact_number', 'is_active']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        employee = super().save(commit=False)
        # Update user info
        employee.user.first_name = self.cleaned_data['first_name']
        employee.user.last_name = self.cleaned_data['last_name']
        employee.user.email = self.cleaned_data['email']
        employee.user.save()
        
        if commit:
            employee.save()
        return employee
