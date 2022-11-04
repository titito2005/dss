from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.urls import reverse

#user registration.
from django.contrib import messages
from authentication.models import Role, User_Role
from .forms import EditUserForm, UserRegisterForm
from .forms import UserLoginForm, LogedChangePasswordForm
from django.contrib.auth.admin import User

#user login.
from django.contrib import auth

#user email
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text

# Account verification.
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Cuenta activada con éxito.')
            return redirect('authentication:login')

        except Exception as ex:
            pass

        return redirect('authentication:login')


# User profile.
class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                return render(request, 'profile.html')
            else:
                messages.warning(request, 'Lo sentimos, no tiene los permisos necesarios para acceder a esta sección.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')


# User login.
class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {'form' : form}
        return render(request, 'login.html', context)

    def post(self, request):
        email = request.POST['username']
        password = request.POST['password']

        if email and password:
            try:
                loginUser = User.objects.get(email = email)
            except:
                messages.warning(request, 'Usuario no registrado.')
                return redirect('authentication:login')
            else:
                if loginUser.is_active == False:
                    messages.warning(request, 'La cuenta se encuentra desactivada.')
                    return redirect('authentication:login')
                else:
                    user = auth.authenticate(username=email, password=password)
                    if user:
                        editRole = User_Role.objects.get(user=user)

                        if editRole:
                            auth.login(request, user)
                            if editRole.changed_password == False:
                                messages.warning(request, 'Por favor cambie la contraseña.')
                                return redirect('authentication:change_password')
                            else:
                                return redirect('main:home')
                        else:
                            messages.warning(request, 'Error al encontrar los datos del usuario.')
                            return redirect('authentication:login')
                    else:         
                        messages.warning(request, 'El nombre de usuario y la contraseña no coinciden.')
                        return redirect('authentication:login')
        else:
            messages.warning(request, 'Por favor rellene todos los espacios.')
            return redirect('authentication:login')


# User register, only for admins.
class RegisterUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = UserRegisterForm()
                context = {'form' : form}
                return render(request, 'register.html', context)
            else:
                messages.warning(request, 'Lo sentimos, no tiene los permisos necesarios para acceder a esta sección.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')
    
    def post(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = UserRegisterForm(request.POST)

                if form.is_valid():
                    verifyUserEmail = User.objects.filter(email = (form.cleaned_data['email'])).exists()
                    if verifyUserEmail:
                        messages.warning(request, 'El correo ingresado ya se encuentra asociado a una cuenta.')
                        form = UserRegisterForm()
                        context = {'form' : form}
                        return render(request, 'register.html', context)
                    else:
                        #User data
                        firstName = form.cleaned_data['first_name']
                        lastName = form.cleaned_data['last_name']
                        userEmail = form.cleaned_data['email']
                        role_form = form.cleaned_data['user_role']
                        userPassword = User.objects.make_random_password(length=12, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')

                        rolequery = Role.objects.filter(name = role_form)
                        if rolequery.count() > 0:

                            role = rolequery[0]
                            newUser = User.objects.create_user(username=userEmail,
                                            email=userEmail,
                                            password=userPassword,
                                            first_name = firstName,
                                            last_name = lastName,
                                            is_active = False)       
                
                            if role.id == 1:
                                newUser.is_superuser = True
                                newUser.is_staff = True
                            else:
                                newUser.is_superuser = False
                                newUser.is_staff = False   

                            #Add user role
                            newRol = User_Role()
                            newRol.user = newUser
                            newRol.role = role
                            newRol.changed_password = False
                            
                            newRol.save()
                            newUser.save()
                            
                            current_site = get_current_site(request)

                            email_body = {
                                'user':  newUser.first_name,
                                'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(newUser.pk)),
                                'token': account_activation_token.make_token(newUser),
                            }

                            link = reverse('authentication:activate', kwargs={'uidb64': email_body['uid'], 'token': email_body['token']})
                            email_subject = 'Active su cuenta en Fertirriego'
                            activate_url = 'http://'+current_site.domain+link
                            email_body_toSend = 'Bienvenido '+newUser.first_name+ ', por favor presione el link para confirmar la creación de su cuenta.\n'+activate_url+ '\n\n Su contraseña temporal es: \n'+ userPassword

                            email = EmailMessage(
                                email_subject,
                                email_body_toSend,
                                'noreply@automaticmail.com',
                                [newUser.email],
                            )

                            email.send(fail_silently=False)

                            messages.success(request, 'Cuenta creada con éxito')
                            return redirect('authentication:admin')
                        
                        else:
                            form = UserRegisterForm()
                            context = {'form' : form}
                            messages.warning(request, 'Rol seleccionado no se encuentra disponible.')
                            return render(request, 'register.html', context)
                            
                else:
                    form = UserRegisterForm()
                    context = {'form' : form}
                    messages.warning(request, 'Por favor rellene todos los espacios.')
                    return render(request, 'register.html', context)
            else:
                messages.warning(request, 'Lo sentimos, no tiene los permisos necesarios para acceder a esta sección.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')  


# Main admin view, only for admins.
class AdminView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                admin_page = User.objects.all()
                return render(request, 'user_admin.html',
                {'admin_page': admin_page,})
            else:
                messages.warning(request, 'Lo sentimos, no tiene los permisos necesarios para acceder a esta sección.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

# User edit, only for admins             
class EditUserView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editUser = User.objects.get(id=id)
                if editUser:
                    userCondition = 0
                    if editUser.is_active:
                        userCondition = 1
                    form = EditUserForm(initial={'user_id': editUser.id, 'email': editUser.email, 'first_name': editUser.first_name, 'last_name': editUser.last_name, 'user_role': editUser.user_role.role, 'user_condition':  userCondition})
                    context = {'form': form}

                    return render(request, 'edit_user.html', context)
                else:
                    messages.warning(request, 'Usuario no encontrado.')
                    return redirect('authentication:admin')
            else:
                messages.warning(request, 'Lo sentimos, no tiene los permisos necesarios para acceder a esta sección.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')
    
    def post(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = EditUserForm(request.POST)
                if form.is_valid():
                    formId = int(form.cleaned_data['user_id'])
                    if formId == id:
                        editUser = User.objects.get(id = formId)
                        if editUser:
                            editRole = User_Role.objects.get(user=formId)
                            if editRole:
                                #Get all new data
                                firstName = form.cleaned_data['first_name']
                                lastName = form.cleaned_data['last_name']
                                userEmail = form.cleaned_data['email']
                                role_form = form.cleaned_data['user_role']
                                condition = form.cleaned_data['user_condition']

                                rolequery = Role.objects.filter(name = role_form)
                                if rolequery.count() > 0:
                                    role = rolequery[0]

                                    editUser.first_name = firstName
                                    editUser.last_name = lastName
                                    editUser.email = userEmail
                                    editUser.username = userEmail
                                    editUser.is_active = condition

                                    if role.id == 1:
                                        editUser.is_superuser = True
                                        editUser.is_staff = True
                                    else:
                                        editUser.is_superuser = False
                                        editUser.is_staff = False

                                    editRole.role = role
                                    editRole.save()
                                    editUser.save()

                                    messages.success(request, 'Cambios realizados correctamente.')
                                    return redirect('authentication:admin')
                                else:
                                    messages.warning(request, 'Rol de usuario no encontrado.')
                                    return redirect('authentication:admin')
                            else:
                                messages.warning(request, 'Usuario no posee roles.')
                                return redirect('authentication:admin')
                        else:
                            messages.warning(request, 'Usuario no encontrado.')
                            return redirect('authentication:admin')
                    else:
                        messages.warning(request, 'Identificador de usuario incorrecto.')
                        return redirect('authentication:admin')
                else:
                    messages.warning(request, 'Error al guardar cambios, rellene todos los espacios.')
                    return redirect('authentication:admin')
            else:
                messages.warning(request, 'Lo sentimos, no tiene los permisos necesarios para acceder a esta sección.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home') 

# User delete, only for admins.            
class DeleteUserView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editUser = User.objects.get(id = id)
                if editUser:
                    editUser.delete()
                    messages.success(request, 'Usuario eliminado con éxito.')
                    return redirect('authentication:admin')
                else:
                    messages.warning(request, 'Error al eliminar el usuario.')
                    return redirect('authentication:admin')
            else:
                messages.warning(request, 'Lo sentimos, no tiene los permisos necesarios para acceder a esta sección.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class LogedChangePasswordView(View):
    def get (self, request):
        if request.user.is_authenticated:
            if request.user.is_active:
                form = LogedChangePasswordForm()
                context = {'form' : form}
                return render(request, 'loged_change_password.html', context)
            else:
                messages.warning(request, 'Usuario inactivo.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Inicie sesión.')
            return redirect('main:home')

    def post (self, request):
        if request.user.is_authenticated:
            if request.user.is_active:
                editUser = User.objects.get(id = request.user.id)
                if editUser:
                    form = LogedChangePasswordForm(request.POST)
                    if form.is_valid():
                        user = auth.authenticate(username=editUser.username, password=form.cleaned_data['past_password'])
                        if user:
                            password1 = form.cleaned_data['new_password']
                            password2 = form.cleaned_data['confirm_password']
                            if password1 == password2:
                                editUser.set_password(password1)
                                editUser.save()
                                editRole = User_Role.objects.get(user=editUser)
                                editRole.changed_password = True
                                editRole.save()
                                
                                #Relogin after change password because is logout
                                user_reloging = auth.authenticate(username=editUser.username, password=password1)
                                auth.login(request, user_reloging)

                                messages.success(request, 'Cambio de contraseña realizado con éxito.')
                                return redirect('main:home')
                            else:
                                messages.warning(request, 'Las contraseñas no coinciden.')
                                return redirect('authentication:change_password')
                        else:
                            messages.warning(request, 'Las contraseña actual no coincide.')
                            return redirect('authentication:change_password')
                    else:
                        context = {'form' : form}
                        return render(request, 'loged_change_password.html', context)
                else:
                    messages.warning(request, 'Usuario no encontrado.')
                    return redirect('main:home')
            else:
                messages.warning(request, 'Usuario inactivo.')
                return redirect('main:home')
        else:
            messages.warning(request, 'Inicie sesión.')
            return redirect('main:home')