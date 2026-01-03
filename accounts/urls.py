from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/save-salary/', views.save_salary_view, name='save_salary'),
]
