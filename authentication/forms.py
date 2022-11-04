from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.password_validation import validate_password
from authentication.models import Role
class UserRegisterForm(forms.Form):
    first_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese el nombre del usuario'}))

    last_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese los apellidos del usuario'}))
    
    email = forms.EmailField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese el correo electrónmico del usuario'}))

    user_role = forms.ModelChoiceField(
        required=True, 
        queryset=Role.objects.all(),
        initial= 0,
        widget=forms.Select(attrs={
            'class': 'drop-button',}))

class LogedChangePasswordForm(forms.Form):
    past_password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese la contraseña actual'}))
    
    new_password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese la nueva contraseña'}), 
            validators=[validate_password])

    confirm_password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'class': 'input-text',
            'placeholder': 'Confirme la nueva contraseña'}))
    
class EditUserForm(UserRegisterForm):
    user_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
             'readonly': ''}))
    
    CONDITION_CHOICES = [
        (1, 'Activo'),
        (0, 'Inactivo')
    ]
    
    user_condition = forms.CharField(
        required=True,
        widget=forms.Select(choices=CONDITION_CHOICES, attrs={
            'class': 'drop-button'}))

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese su correo electrónico'}))

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
        'class': 'input-text',
        'placeholder': 'Ingrese su contraseña'}))
    class Meta:
        model = User
        fields = ['email', 'password']
        help_texts = {j:"" for j in fields}