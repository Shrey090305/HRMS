from django.db import models
from django.db.models import F, Sum, ExpressionWrapper, IntegerField
from employees.models import Employee
from datetime import timedelta


class LeaveAllocation(models.Model):
    """
    Leave allocation for employees - tracks available leave days
    """
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='leave_allocation')
    paid_time_off = models.IntegerField(default=24, help_text="Annual paid leave days")
    sick_time_off = models.IntegerField(default=7, help_text="Sick leave days")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leave_allocations'
    
    def __str__(self):
        return f"{self.employee.employee_id} - PTO: {self.paid_time_off}, Sick: {self.sick_time_off}"
    
    @property
    def paid_time_off_used(self):
        """Calculate used paid time off"""
        from django.db.models.functions import Coalesce
        leaves = LeaveRequest.objects.filter(
            employee=self.employee,
            leave_type__in=['annual', 'casual'],
            status='approved'
        )
        total_days = 0
        for leave in leaves:
            total_days += (leave.end_date - leave.start_date).days + 1
        return total_days
    
    @property
    def sick_time_off_used(self):
        """Calculate used sick time off"""
        leaves = LeaveRequest.objects.filter(
            employee=self.employee,
            leave_type='sick',
            status='approved'
        )
        total_days = 0
        for leave in leaves:
            total_days += (leave.end_date - leave.start_date).days + 1
        return total_days
    
    @property
    def paid_time_off_available(self):
        """Calculate available paid time off"""
        return max(0, self.paid_time_off - self.paid_time_off_used)
    
    @property
    def sick_time_off_available(self):
        """Calculate available sick time off"""
        return max(0, self.sick_time_off - self.sick_time_off_used)


class LeaveRequest(models.Model):
    """
    Leave request model for employees.
    """
    LEAVE_TYPE_CHOICES = (
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('annual', 'Annual Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('unpaid', 'Unpaid Leave'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    attachment = models.FileField(upload_to='leave_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leave_requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type} ({self.start_date} to {self.end_date})"
    
    @property
    def duration_days(self):
        """Calculate leave duration in days"""
        delta = self.end_date - self.start_date
        return delta.days + 1
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'
