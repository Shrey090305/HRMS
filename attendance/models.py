from django.db import models
from employees.models import Employee


class Attendance(models.Model):
    """
    Attendance record for employees.
    Tracks check-in, check-out times and status.
    """
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half-day', 'Half Day'),
        ('on-leave', 'On Leave'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'attendance'
        ordering = ['-date']
        unique_together = ['employee', 'date']
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} ({self.status})"
    
    @property
    def working_hours(self):
        """Calculate working hours"""
        if self.check_in_time and self.check_out_time:
            from datetime import datetime, timedelta
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            delta = check_out - check_in
            hours = delta.total_seconds() / 3600
            return round(hours, 2)
        return 0
    
    @property
    def work_hours(self):
        """Return formatted work hours (HH:MM)"""
        if self.check_in_time and self.check_out_time:
            from datetime import datetime
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            
            # Subtract break time if employee has it configured
            break_hours = 0
            if hasattr(self.employee, 'break_time_hours') and self.employee.break_time_hours:
                break_hours = float(self.employee.break_time_hours)
            
            delta = check_out - check_in
            total_hours = delta.total_seconds() / 3600
            work_hours = total_hours - break_hours
            
            hours = int(work_hours)
            minutes = int((work_hours - hours) * 60)
            return f"{hours:02d}:{minutes:02d}"
        return "00:00"
    
    @property
    def extra_hours(self):
        """Calculate extra hours beyond standard 9-hour workday"""
        if self.check_in_time and self.check_out_time:
            from datetime import datetime
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            
            # Subtract break time
            break_hours = 0
            if hasattr(self.employee, 'break_time_hours') and self.employee.break_time_hours:
                break_hours = float(self.employee.break_time_hours)
            
            delta = check_out - check_in
            total_hours = delta.total_seconds() / 3600
            work_hours = total_hours - break_hours
            
            # Standard work hours is 9 hours
            standard_hours = 9.0
            extra = max(0, work_hours - standard_hours)
            
            hours = int(extra)
            minutes = int((extra - hours) * 60)
            return f"{hours:02d}:{minutes:02d}"
        return "00:00"
    
    @property
    def is_payable_day(self):
        """Check if this day should be counted for payslip calculation"""
        # Present days are payable
        if self.status == 'present':
            return True
        # Half-day counts as 0.5
        elif self.status == 'half-day':
            return 0.5
        # Paid leaves are payable (check leave table)
        elif self.status == 'on-leave':
            # Check if it's a paid leave
            from leave.models import LeaveRequest
            leave = LeaveRequest.objects.filter(
                employee=self.employee,
                start_date__lte=self.date,
                end_date__gte=self.date,
                status='approved'
            ).first()
            if leave and leave.leave_type in ['annual', 'sick', 'casual']:  # These are typically paid
                return True
        # Absent and unpaid leaves are not payable
        return False
