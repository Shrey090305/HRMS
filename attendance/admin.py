from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in_time', 'check_out_time', 'status', 'working_hours')
    list_filter = ('status', 'date')
    search_fields = ('employee__employee_id', 'employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'date'
    
    def working_hours(self, obj):
        return obj.working_hours
    working_hours.short_description = 'Working Hours'
