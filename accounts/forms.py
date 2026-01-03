from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignUpForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Full Name'
    }))
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'type': 'password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'type': 'password'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Auto-generate username from email
        user.username = self.cleaned_data['email'].split('@')[0]
        # Handle duplicate usernames
        base_username = user.username
        counter = 1
        while User.objects.filter(username=user.username).exists():
            user.username = f"{base_username}{counter}"
            counter += 1
        
        # Split first_name into first and last name if possible
        name_parts = self.cleaned_data['first_name'].strip().split()
        if len(name_parts) >= 2:
            user.first_name = name_parts[0]
            user.last_name = ' '.join(name_parts[1:])
        else:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = ''
        
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user


class SignInForm(AuthenticationForm):
    """Form for user login"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
