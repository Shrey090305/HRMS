from django import forms
from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):
    """Form for applying leave"""
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError('End date must be after start date.')
        
        return cleaned_data


class LeaveApprovalForm(forms.ModelForm):
    """Form for approving/rejecting leave requests"""
    class Meta:
        model = LeaveRequest
        fields = ['status', 'admin_remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'admin_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LeaveFilterForm(forms.Form):
    """Form for filtering leave requests"""
    leave_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + list(LeaveRequest.LEAVE_TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + list(LeaveRequest.STATUS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
