from django.contrib import admin
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'duration_days', 'status', 'created_at')
    list_filter = ('leave_type', 'status', 'start_date')
    search_fields = ('employee__employee_id', 'employee__user__first_name', 'employee__user__last_name', 'reason')
    date_hierarchy = 'start_date'
    
    def duration_days(self, obj):
        return obj.duration_days
    duration_days.short_description = 'Duration (days)'
