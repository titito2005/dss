from django import template
from django.urls import path
from django.urls.base import reverse_lazy

#Local views
from . import views
from .views import VerificationView, LoginView, AdminView, EditUserView 
from .views import DeleteUserView, RegisterUserView, LogedChangePasswordView

#Django views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

#namespace
app_name = 'authentication'

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(template_name ='logout.html'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    #Loged change password (first time)
    path('change_password/', LogedChangePasswordView.as_view(), name='change_password'),
    #Confirm user email
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'), 
    #Forgot password
    path('reset_password/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('authentication:password_reset_done'),
        email_template_name='base_forgotPassword.html',
        template_name ='password_reset.html'), name='reset_password'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(
         template_name ='password_reset_done.html',
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('authentication:password_reset_complete'),
        template_name ='new_password_reset.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name ='password_reset_complete.html'), name='password_reset_complete'),
    #Admin paths
    path('admin/', AdminView.as_view(), name='admin'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('admin/edit/<int:id>/', EditUserView.as_view(), name='edit_user'),
    path('admin/delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),
]