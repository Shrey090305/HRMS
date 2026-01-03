from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'department', 'designation', 'employment_type', 'is_active')
    list_filter = ('department', 'employment_type', 'is_active')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'designation')
    date_hierarchy = 'date_of_joining'
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
