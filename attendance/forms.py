from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):
    """Form for marking attendance"""
    class Meta:
        model = Attendance
        fields = ['date', 'check_in_time', 'check_out_time', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AttendanceFilterForm(forms.Form):
    """Form for filtering attendance records"""
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + list(Attendance.STATUS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
