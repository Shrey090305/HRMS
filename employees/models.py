from django.db import models
from accounts.models import User


class Employee(models.Model):
    """
    Extended employee information model.
    Links to User model for authentication.
    """
    DEPARTMENT_CHOICES = (
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Sales', 'Sales'),
        ('Marketing', 'Marketing'),
        ('Operations', 'Operations'),
    )
    
    EMPLOYMENT_TYPE_CHOICES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('intern', 'Intern'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    designation = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full-time')
    date_of_joining = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Salary Information Fields
    monthly_wage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    yearly_wage = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    working_days_per_week = models.IntegerField(null=True, blank=True, default=5)
    break_time_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=1.0)
    
    # Salary Components (will be auto-calculated)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    standard_allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=4167.00)
    performance_bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fixed_allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # PF Contribution
    pf_employee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pf_employer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Tax Deductions
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=200.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employees'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()
    
    def get_payable_days(self, start_date, end_date):
        """
        Calculate total payable days for payslip generation
        based on attendance records within the date range.
        This considers:
        - Present days (full day = 1)
        - Half days (0.5)
        - Paid leaves (annual, sick, casual = 1)
        - Unpaid leaves and absences (0)
        """
        from attendance.models import Attendance
        
        attendance_records = Attendance.objects.filter(
            employee=self,
            date__gte=start_date,
            date__lte=end_date
        )
        
        payable_days = 0
        for record in attendance_records:
            payable = record.is_payable_day
            if payable == True:
                payable_days += 1
            elif isinstance(payable, float):
                payable_days += payable
        
        return payable_days
    
    def calculate_prorated_salary(self, start_date, end_date):
        """
        Calculate prorated salary based on payable days.
        Returns a dictionary with breakdown of salary components.
        """
        from datetime import timedelta
        
        # Get total days in the month
        if start_date.month == 12:
            month_end = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
        
        total_days_in_month = month_end.day
        payable_days = self.get_payable_days(start_date, end_date)
        
        # Calculate proration factor
        proration_factor = payable_days / total_days_in_month if total_days_in_month > 0 else 0
        
        # Calculate prorated components
        prorated_salary = {
            'payable_days': payable_days,
            'total_days': total_days_in_month,
            'proration_factor': round(proration_factor, 4),
            'basic_salary': float(self.basic_salary or 0) * proration_factor if self.basic_salary else 0,
            'hra': float(self.hra or 0) * proration_factor if self.hra else 0,
            'standard_allowance': float(self.standard_allowance or 0) * proration_factor if self.standard_allowance else 0,
            'performance_bonus': float(self.performance_bonus or 0) * proration_factor if self.performance_bonus else 0,
            'lta': float(self.lta or 0) * proration_factor if self.lta else 0,
            'fixed_allowance': float(self.fixed_allowance or 0) * proration_factor if self.fixed_allowance else 0,
            'gross_salary': float(self.monthly_wage or 0) * proration_factor if self.monthly_wage else 0,
        }
        
        # Calculate deductions (these are typically not prorated)
        prorated_salary['pf_employee'] = float(self.pf_employee or 0)
        prorated_salary['professional_tax'] = float(self.professional_tax or 0)
        
        # Calculate net salary
        prorated_salary['total_deductions'] = prorated_salary['pf_employee'] + prorated_salary['professional_tax']
        prorated_salary['net_salary'] = prorated_salary['gross_salary'] - prorated_salary['total_deductions']
        
        return prorated_salary
