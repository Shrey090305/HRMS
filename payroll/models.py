from django.db import models
from employees.models import Employee


class Payroll(models.Model):
    """
    Payroll records for employees.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payroll'
        ordering = ['-year', '-month']
        unique_together = ['employee', 'month', 'year']
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.month}/{self.year}"
    
    def save(self, *args, **kwargs):
        # Calculate net salary
        self.net_salary = (
            self.basic_salary + 
            self.allowances + 
            self.bonus + 
            self.overtime_pay - 
            self.deductions
        )
        super().save(*args, **kwargs)
    
    @property
    def month_name(self):
        """Get month name"""
        from calendar import month_name
        return month_name[self.month]
    
    @property
    def gross_salary(self):
        """Calculate gross salary"""
        return self.basic_salary + self.allowances + self.bonus + self.overtime_pay


class PayrollComponent(models.Model):
    """
    Additional payroll components (allowances/deductions).
    """
    COMPONENT_TYPE_CHOICES = (
        ('allowance', 'Allowance'),
        ('deduction', 'Deduction'),
    )
    
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='components')
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'payroll_components'
    
    def __str__(self):
        return f"{self.payroll} - {self.name} ({self.component_type})"
