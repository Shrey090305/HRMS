from django.contrib import admin
from .models import Payroll, PayrollComponent


class PayrollComponentInline(admin.TabularInline):
    model = PayrollComponent
    extra = 1


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month_name', 'year', 'gross_salary', 'net_salary', 'is_paid', 'payment_date')
    list_filter = ('year', 'month', 'is_paid')
    search_fields = ('employee__employee_id', 'employee__user__first_name', 'employee__user__last_name')
    inlines = [PayrollComponentInline]
    
    def month_name(self, obj):
        return obj.month_name
    month_name.short_description = 'Month'


@admin.register(PayrollComponent)
class PayrollComponentAdmin(admin.ModelAdmin):
    list_display = ('payroll', 'component_type', 'name', 'amount')
    list_filter = ('component_type',)
    search_fields = ('name', 'payroll__employee__employee_id')
