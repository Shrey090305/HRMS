from django import forms
from .models import Payroll, PayrollComponent


class PayrollForm(forms.ModelForm):
    """Form for creating/editing payroll"""
    class Meta:
        model = Payroll
        fields = ['employee', 'month', 'year', 'basic_salary', 'allowances', 
                  'deductions', 'bonus', 'overtime_pay', 'payment_date', 'is_paid', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'allowances': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deductions': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'overtime_pay': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PayrollFilterForm(forms.Form):
    """Form for filtering payroll records"""
    month = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Month (1-12)', 'min': 1, 'max': 12})
    )
    year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'})
    )
    is_paid = forms.ChoiceField(
        required=False,
        choices=[('', 'All'), ('true', 'Paid'), ('false', 'Unpaid')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
