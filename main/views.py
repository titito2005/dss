from ast import Add
from operator import add
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from main.models import Greenhouse_Database_Connection, Crop_Limits
from main.models import Agronomic_Indicator, Monitoring, Physical_Variable, Variable_Type
from main.models import Greenhouse, Crop, Physical_Variable, Variable_Type
from main.forms import AddCropForm, AddGreenHouseForm, AddMonitoringForm, AddPhysicalVarForm, AddIndicatorForm, EditCropForm, EditLimitForm
from main.forms import GreenHouseConfigForm, EditGreenHouseForm, EditIndicatorForm, EditMonitoringForm, EditPhysicalVarForm, AddLimitForm
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class MonitoringView(View):
    def get(self, request):
        return render(request, 'monitoring.html')

class MonitoringsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                monitoring_page = Monitoring.objects.all()
            else:
                monitoring_page = Monitoring.objects.filter(created_by = request.user)
            return render(request, 'monitorings.html',
            {'monitoring_page': monitoring_page})
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class AddMonitoringView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = AddMonitoringForm(id=0)
            else:
                form = AddMonitoringForm(id=request.user.id)
            completeVariableTypes = Variable_Type.objects.all()
            completeVariables = Physical_Variable.objects.all()
            for type in completeVariableTypes:
                found = False
                for variable in completeVariables:
                    if variable.type == type:
                        found = True
                if found == False:
                    completeVariableTypes = completeVariableTypes.exclude(name=type)
            context = {"form": form, "completeVariables": completeVariables, "completeVariableTypes": completeVariableTypes}
            return render(request, 'add_monitoring.html', context)
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request):
        if request.user.is_authenticated:
            form = AddMonitoringForm(request.POST, id=0)
            if form.is_valid():
                messages.success(request, 'Estación de monitorización creada con éxito.')
                monitoring = Monitoring()
                monitoring.greenhouse = form.cleaned_data['greenhouse']
                monitoring.type = form.cleaned_data['type']
                monitoring.created_by = request.user
                monitoring.save()
                monitoring.sensors.add(*form.cleaned_data['variables'])
                return redirect('main:monitorings')
            else:
                messages.warning(request, 'Error registrando los datos, rellene todos los espacios.')
                context = {'form' : form}
                return render(request, 'add_monitoring.html', context)
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')


class EditMonitoringView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            editMonitoring = Monitoring.objects.get(id=id)
            if editMonitoring:
                form = EditMonitoringForm(id=0, initial={'monitoring_id':editMonitoring.id, 'greenhouse': editMonitoring.greenhouse, 'type': editMonitoring.type})
                phys_vars = editMonitoring.sensors.all()
                form.fields['variables'].initial = phys_vars
                context = {'form': form}
                return render(request, 'edit_monitoring.html', context)
            else:
                messages.warning(request, 'Estación de monitorización no encontrada.')
                return redirect('main:indicator')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request, id):
        if request.user.is_authenticated:
            form = EditMonitoringForm(request.POST, id=0)
            if form.is_valid():
                formId = int(form.cleaned_data['monitoring_id'])
                if formId == id:
                    editMonitoring = Monitoring.objects.get(id = formId)
                    if editMonitoring:
                        #Get all new data
                        editMonitoring.greenhouse = form.cleaned_data['greenhouse']
                        editMonitoring.type = form.cleaned_data['type']
                        editMonitoring.created_by = request.user
                        editMonitoring.save()
                        editMonitoring.sensors.clear()
                        editMonitoring.sensors.add(*form.cleaned_data['variables'])
                        messages.success(request, 'Cambios realizados correctamente.')
                        return redirect('main:monitorings')
                    else:
                        messages.warning(request, 'Estación de monitorización no encontrado.')
                        return redirect('main:monitorings')
                else:
                    messages.warning(request, 'Identificador de la estación de monitorización incorrecto.')
                    return redirect('main:monitorings')
            else:
                messages.warning(request, 'Error al guardar cambios, rellene todos los espacios.')
                return redirect('main:monitorings')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class DeleteMonitoringView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            editMonitoring = Monitoring.objects.get(id = id)
            if editMonitoring:
                editMonitoring.delete()
                messages.success(request, 'Estación de monitorización eliminada con éxito.')
                return redirect('main:monitorings')
            else:
                messages.warning(request, 'Error al eliminar la Estación de monitorización.')
                return redirect('main:monitorings')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class PhysVarView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                phys_page = Physical_Variable.objects.all()
                return render(request, 'phys_var.html',
                {'phys_page': phys_page})
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')  
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class AddPhysicalVarView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = AddPhysicalVarForm()
                context = {'form': form}
                return render(request, 'add_phys_var.html', context)
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')  
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self,request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = AddPhysicalVarForm(request.POST)
                if form.is_valid():
                    messages.success(request, 'Variable física creada con éxito.')
                    variable = Physical_Variable()
                    variable.name = form.cleaned_data['name']
                    variable.description = form.cleaned_data['description']
                    variable.unit_of_measurement = form.cleaned_data['unit_of_measurement']
                    variable.type = form.cleaned_data['type']
                    variable.created_by = request.user
                    variable.save()
                    return redirect('main:phys_var')
                else:
                    messages.warning(request, 'Error registrando los datos, rellene todos los espacios.')
                    context = {'form' : form}
                    return render(request, 'phys_var.html', context)
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')  
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class EditPhysicalVarView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editPhys = Physical_Variable.objects.get(id=id)
                if editPhys:
                    form = EditPhysicalVarForm(initial={'physical_id':editPhys.id, 'name': editPhys.name, 'description': editPhys.description, 'unit_of_measurement': editPhys.unit_of_measurement, 'type': editPhys.type})
                    context = {'form': form}
                    return render(request, 'edit_phys_var.html', context)
                else:
                    messages.warning(request, 'Variable física no encontrada.')
                    return redirect('main:phys_var')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')  
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = EditPhysicalVarForm(request.POST)
                if form.is_valid():
                    formId = int(form.cleaned_data['physical_id'])
                    if formId == id:
                        editPhys = Physical_Variable.objects.get(id = formId)
                        if editPhys:
                            #Get all new data
                            name = form.cleaned_data['name']
                            description = form.cleaned_data['description']
                            unit_of_measurement = form.cleaned_data['unit_of_measurement']
                            type = form.cleaned_data['type']
                            editPhys.name = name
                            editPhys.description = description
                            editPhys.unit_of_measurement = unit_of_measurement
                            editPhys.type = Variable_Type.objects.get(name = type)
                            editPhys.save()
                            messages.success(request, 'Cambios realizados correctamente.')
                            return redirect('main:phys_var')
                        else:
                            messages.warning(request, 'Invernadero no encontrado.')
                            return redirect('main:phys_var')
                    else:
                        messages.warning(request, 'Identificador de invernadero incorrecto.')
                        return redirect('main:phys_var')
                else:
                    messages.warning(request, 'Error al guardar cambios, rellene todos los espacios.')
                    return redirect('main:phys_var')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')  
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class DeletePhysicalVarView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editPhys = Physical_Variable.objects.get(id = id)
                if editPhys:
                    editPhys.delete()
                    messages.success(request, 'Variable física eliminada con éxito.')
                    return redirect('main:phys_var')
                else:
                    messages.warning(request, 'Error al eliminar la variable física.')
                    return redirect('main:phys_var')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')  
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class AgronomicIndicatorView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                indicator_page = Agronomic_Indicator.objects.all()
                return render(request, 'agronomic_indicator.html',
                {'indicator_page': indicator_page})
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')               
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class AddIndicatorView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                completeVariables = Physical_Variable.objects.all()
                form = AddIndicatorForm(id=0)
                completeVariableTypes = Variable_Type.objects.all()
                for type in completeVariableTypes:
                    found = False
                    for variable in completeVariables:
                        if variable.type == type:
                            found = True
                    if found == False:
                        completeVariableTypes = completeVariableTypes.exclude(name=type)
                context = {"form": form, "completeVariables": completeVariables, "completeVariableTypes": completeVariableTypes}
                return render(request, 'add_indicator.html', context)
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')    
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = AddIndicatorForm(request.POST, id=0)
                if form.is_valid():
                    messages.success(request, 'Indicador agronómico creado con éxito.')
                    indicator = Agronomic_Indicator()
                    indicator.name = form.cleaned_data['name']
                    indicator.description = form.cleaned_data['description']
                    indicator.unit_of_measurement = form.cleaned_data['unit_of_measurement']
                    indicator.created_by = request.user
                    indicator.save()
                    indicator.phys_vars.add(*form.cleaned_data['variables'])
                    return redirect('main:indicator')
                else:
                    messages.warning(request, 'Error registrando el indicador agronómico, rellene todos los espacios.')
                    context = {'form' : form}
                    return render(request, 'add_indicator.html', context)
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home')  
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class EditIndicatorView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            editIndicator = Agronomic_Indicator.objects.get(id=id)
            if editIndicator:
                if request.user.user_role.role.id == 1:
                    form = EditIndicatorForm(id=0, initial={'indicator_id':editIndicator.id, 'name': editIndicator.name, 'description': editIndicator.description, 'unit_of_measurement': editIndicator.unit_of_measurement})
                    phys_vars = editIndicator.phys_vars.all()
                    form.fields['variables'].initial = phys_vars
                    context = {'form': form}
                    return render(request, 'edit_indicator.html', context)
                else:
                    messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                    return redirect('main:home')  
            else:
                messages.warning(request, 'Indicador agronómico no encontrada.')
                return redirect('main:indicator')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = EditIndicatorForm(request.POST, id=0)
                if form.is_valid():
                    formId = int(form.cleaned_data['indicator_id'])
                    if formId == id:
                        editIndicator = Agronomic_Indicator.objects.get(id = formId)
                        if editIndicator:
                            #Get all new data
                            editIndicator.name = form.cleaned_data['name']
                            editIndicator.description = form.cleaned_data['description']
                            editIndicator.unit_of_measurement = form.cleaned_data['unit_of_measurement']
                            editIndicator.save()
                            editIndicator.phys_vars.clear()
                            editIndicator.phys_vars.add(*form.cleaned_data['variables'])
                            messages.success(request, 'Cambios realizados correctamente.')
                            return redirect('main:indicator')
                        else:
                            messages.warning(request, 'Indicador agronómico no encontrado.')
                            return redirect('main:indicator')
                    else:
                        messages.warning(request, 'Identificador de indicador agronómico incorrecto.')
                        return redirect('main:indicator')
                else:
                    messages.warning(request, 'Error al guardar cambios, rellene todos los espacios.')
                    return redirect('main:indicator')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class DeleteIndicatorView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editIndicator = Agronomic_Indicator.objects.get(id = id)
                if editIndicator:
                    editIndicator.phys_vars.clear()
                    editIndicator.delete()
                    messages.success(request, 'Indicador agronómico eliminado con éxito.')
                    return redirect('main:indicator')
                else:
                    messages.warning(request, 'Error al eliminar el indicador agronómico.')
                    return redirect('main:indicator')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class GreenhousesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                greenhouse_page = Greenhouse.objects.all()
            else:
                greenhouse_page = Greenhouse.objects.filter(created_by = request.user)
            return render(request, 'greenhouses.html',
            {'greenhouse_page': greenhouse_page})
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class GreenhouseDetailsView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            greenhouse = Greenhouse.objects.get(id=id)
            monitorings = Monitoring.objects.filter(greenhouse = greenhouse)
            return render(request, 'greenhouse_details.html', {'greenhouse': greenhouse, 'monitorings': monitorings})
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class AddGreenhouseView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = AddGreenHouseForm(id=0)
            context = {'form' : form}
            return render(request, 'add_greenhouse.html', context)
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request):
        if request.user.is_authenticated:
            form = AddGreenHouseForm(request.POST, id=0)
            if form.is_valid():
                messages.success(request, 'Invernadero creado con éxito.')
                greenhouse = Greenhouse()
                greenhouse.location=form.cleaned_data['location']
                greenhouse.crop=form.cleaned_data['crop']
                greenhouse.start_date=form.cleaned_data['start_date']
                greenhouse.owner = form.cleaned_data['owner']
                greenhouse.created_by = request.user
                greenhouse.save()
                #Creacion de los datos de conexion vacios.
                greenhouseConnection = Greenhouse_Database_Connection()
                greenhouseConnection.greenhouse = greenhouse
                greenhouseConnection.save()
                return redirect('main:greenhouses')
            else:
                messages.warning(request, 'Error registrando los datos, rellene todos los espacios.')
                context = {'form' : form}
                return render(request, 'add_phys_var.html', context)
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class EditGreenhouseView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            editGreenhouse = Greenhouse.objects.get(id=id)
            if editGreenhouse:
                form = EditGreenHouseForm(id=0, initial={'greenhouse_id':editGreenhouse.id, 'owner':editGreenhouse.owner,'location': editGreenhouse.location, 'crop': editGreenhouse.crop, 'start_date': editGreenhouse.start_date})
                context = {'form': form}
                return render(request, 'edit_greenhouse.html', context)
            else:
                messages.warning(request, 'Invernadero no encontrado.')
                return redirect('main:greenhouses')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request, id):
        if request.user.is_authenticated:
            form = EditGreenHouseForm(request.POST, id=0)
            if form.is_valid():
                formId = int(form.cleaned_data['greenhouse_id'])
                if formId == id:
                    editGreenhouse = Greenhouse.objects.get(id = formId)
                    if editGreenhouse:
                        #Get all new data
                        location = form.cleaned_data['location']
                        owner = form.cleaned_data['owner']
                        crop = form.cleaned_data['crop']
                        start_date = form.cleaned_data['start_date']
                        editGreenhouse.location = location
                        editGreenhouse.owner = owner
                        editGreenhouse.crop = crop
                        editGreenhouse.start_date = start_date
                        editGreenhouse.save()
                        messages.success(request, 'Cambios realizados correctamente.')
                        return redirect('main:greenhouses')
                    else:
                        messages.warning(request, 'Invernadero no encontrado.')
                        return redirect('main:greenhouses')
                else:
                    messages.warning(request, 'Identificador de invernadero incorrecto.')
                    return redirect('main:greenhouses')
            else:
                messages.warning(request, 'Error al guardar cambios, rellene todos los espacios.')
                return redirect('main:greenhouses')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class DeleteGreenhouseView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            editGreenhouse = Greenhouse.objects.get(id = id)
            if editGreenhouse:
                editGreenhouse.delete()
                messages.success(request, 'Invernadero eliminado con éxito.')
                return redirect('main:greenhouses')
            else:
                messages.warning(request, 'Error al eliminar el invernadero.')
                return redirect('main:greenhouses')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class ConfigGreenhouseView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            greenhouse = Greenhouse.objects.get(id=id)
            greenhouseConfig = Greenhouse_Database_Connection.objects.get(greenhouse = greenhouse)
            if (greenhouse and greenhouseConfig):
                form = GreenHouseConfigForm(initial={'greenhouse':greenhouse, 
                'url':greenhouseConfig.url,
                'ip':greenhouseConfig.ip,
                'database_name':greenhouseConfig.database_name,
                'table_name':greenhouseConfig.table_name, 
                'user':greenhouseConfig.user,
                'password':greenhouseConfig.password})
                context = {'form':form, 'greenhouse':greenhouse}
                return render(request, 'greenhouse_config.html', context)
            else:
                messages.warning(request, 'Error al encontrar el invernadero.')
                return redirect('main:greenhouses')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')
    
    def post(self, request, id):
        if request.user.is_authenticated:
            form = GreenHouseConfigForm(request.POST)
            if form.is_valid():
                greenhouse = Greenhouse.objects.get(id=id)
                greenhouseConfig = Greenhouse_Database_Connection.objects.get(greenhouse = greenhouse)
                if (greenhouse and greenhouseConfig):
                    greenhouseConfig.url = form.cleaned_data['url']
                    greenhouseConfig.ip = form.cleaned_data['ip']
                    greenhouseConfig.database_name = form.cleaned_data['database_name']   
                    greenhouseConfig.table_name = form.cleaned_data['table_name']
                    greenhouseConfig.user = form.cleaned_data['user']
                    greenhouseConfig.password = form.cleaned_data['password']
                    greenhouseConfig.save()
                    messages.success(request, 'Cambios realizados correctamente.')
                    return redirect('main:greenhouses')
                else:
                    messages.warning(request, 'Error al encontrar el invernadero.')
                    return redirect('main:greenhouses')
            else:
                context = {'form' : form}
                messages.warning(request, 'Error validando el formulario, rellene todos los espacios.')
                return render(request, 'greenhouse_config.html', context)
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')                                                         

class GreenhouseDataView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            greenhouse = Greenhouse.objects.get(id=id)
            if (greenhouse):
                allSensors = []
                allIndicators = []
                monitorings = Monitoring.objects.filter(greenhouse = greenhouse)
                agronomicIndicators = Agronomic_Indicator.objects.all()

                for monitoring in monitorings:
                    sensors = monitoring.sensors.all()
                    for agronomicIndicator in agronomicIndicators:
                        indicators = agronomicIndicator.phys_vars.all()
                        addIndicator = True
                        for indicator in indicators:
                            if indicator not in sensors:
                                addIndicator = False
                        
                        if addIndicator and addIndicator not in allIndicators:
                            allIndicators.append(agronomicIndicator)

                    for sensor in sensors:
                        limit = Crop_Limits.objects.filter(crop = greenhouse.crop, phys_vars = sensor)
                        if limit:
                            sensor.limit = limit[0]
                        allSensors.append(sensor)
                
                return render(request, 'greenhouse_data_display.html', {'greenhouse': greenhouse, 'allSensors': allSensors, 'allIndicators': allIndicators})
            messages.warning(request, 'No se ha encontrado el invernadero.')
            return redirect('main:greenhouses')
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class CropsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                crop_page = Crop.objects.all()
                return render(request, 'crops.html',
                {'crop_page': crop_page})
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class AddCropsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = AddCropForm()
                context = {"form": form}
                return render(request, 'add_crops.html', context)
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = AddCropForm(request.POST)
                if form.is_valid():
                    crop = Crop()
                    crop.name = form.cleaned_data['name']
                    crop.description = form.cleaned_data['description']
                    crop.created_by = request.user
                    crop.save()
                    messages.success(request, 'Cultivo creado con éxito.')
                    return redirect('main:crops')
                else:
                    messages.warning(request, 'Error registrando el cultivo, rellene todos los espacios.')
                    context = {'form' : form}
                    return render(request, 'add_crops.html', context)
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class EditCropView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editCrop = Crop.objects.get(id=id)
                if editCrop:
                    form = EditCropForm(initial={'crop_id':editCrop.id, 'name': editCrop.name, 'description': editCrop.description})
                    context = {'form': form}
                    return render(request, 'edit_crop.html', context)
                else:
                    messages.warning(request, 'Cultivo no encontrado.')
                    return redirect('main:crops')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = EditCropForm(request.POST)
                if form.is_valid():
                    formId = int(form.cleaned_data['crop_id'])
                    if formId == id:
                        editCrop = Crop.objects.get(id = formId)
                        if editCrop:
                            #Get all new data
                            name = form.cleaned_data['name']
                            description = form.cleaned_data['description']
                            editCrop.name = name
                            editCrop.description = description
                            editCrop.save()
                            messages.success(request, 'Cambios realizados correctamente.')
                            return redirect('main:crops')
                        else:
                            messages.warning(request, 'Cultivo no encontrado.')
                            return redirect('main:crops')
                    else:
                        messages.warning(request, 'Identificador de cultivo incorrecto.')
                        return redirect('main:crops')
                else:
                    messages.warning(request, 'Error al guardar cambios, rellene todos los espacios.')
                    return redirect('main:crops')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class DeleteCropView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editCrop = Crop.objects.get(id = id)
                if editCrop:
                    editCrop.delete()
                    messages.success(request, 'Cultivo eliminado con éxito.')
                    return redirect('main:crops')
                else:
                    messages.warning(request, 'Error al eliminar el cultivo.')
                    return redirect('main:crops')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class LimitsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                limits_page = Crop_Limits.objects.all()
                return render(request, 'limits.html',
                {'limits_page': limits_page})
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class AddLimitView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = AddLimitForm()
                context = {"form": form}
                return render(request, 'add_limit.html', context)
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = AddLimitForm(request.POST)
                if form.is_valid():
                    try:
                        limit = Crop_Limits()
                        limit.crop = form.cleaned_data['crop']
                        limit.phys_vars = form.cleaned_data['phys_vars']
                        limit.max_limit = form.cleaned_data['max_limit']
                        limit.min_limit = form.cleaned_data['min_limit']                
                        limit.save()
                        messages.success(request, 'Limite creado con éxito.')
                        return redirect('main:limits')
                    except:
                        messages.warning(request, 'Ya existe este límite.')
                        context = {'form' : form}
                        return render(request, 'add_limit.html', context)
                else:
                    messages.warning(request, 'Error registrando el limite, rellene todos los espacios.')
                    context = {'form' : form}
                    return render(request, 'add_limit.html', context)
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class EditLimitView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editLimit = Crop_Limits.objects.get(id=id)
                if editLimit:
                    form = EditLimitForm(initial={'limit_id':editLimit.id, 'crop': editLimit.crop, 'phys_vars': editLimit.phys_vars, 'max_limit': editLimit.max_limit, 'min_limit': editLimit.min_limit})
                    context = {'form': form}
                    return render(request, 'edit_limit.html', context)
                else:
                    messages.warning(request, 'Límite no encontrado.')
                    return redirect('main:limits')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

    def post(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                form = EditLimitForm(request.POST)
                if form.is_valid():
                    formId = int(form.cleaned_data['limit_id'])
                    if formId == id:
                        editLimit = Crop_Limits.objects.get(id = formId)
                        if editLimit:
                            try:
                                editLimit.crop = form.cleaned_data['crop']
                                editLimit.phys_vars = form.cleaned_data['phys_vars']
                                editLimit.max_limit = form.cleaned_data['max_limit']
                                editLimit.min_limit = form.cleaned_data['min_limit']                
                                editLimit.save()
                                messages.success(request, 'Cambios realizados correctamente.')
                                return redirect('main:limits')
                            except:
                                messages.warning(request, 'Ya existe este límite.')
                                context = {'form' : form}
                                return render(request, 'edit_limit.html', context)
                        else:
                            messages.warning(request, 'Límite no encontrado.')
                            return redirect('main:limits')
                    else:
                        messages.warning(request, 'Identificador de límite incorrecto.')
                        return redirect('main:limits')
                else:
                    messages.warning(request, 'Error al guardar cambios, rellene todos los espacios.')
                    return redirect('main:limits')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class DeleteLimitView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.user_role.role.id == 1:
                editLimit = Crop_Limits.objects.get(id = id)
                if editLimit:
                    editLimit.delete()
                    messages.success(request, 'Limite eliminado con éxito.')
                    return redirect('main:limits')
                else:
                    messages.warning(request, 'Error al eliminar el límite.')
                    return redirect('main:limits')
            else:
                messages.warning(request, 'No tiene los permisos para acceder a esta sección.')
                return redirect('main:home') 
        else:
            messages.warning(request, 'Es necesario iniciar sesión para acceder a esta sección.')
            return redirect('main:home')

class DataView(View):
    def get(self, request, id):
        greenhouse = Greenhouse.objects.get(id=id)
        if(greenhouse):
            data = {}
            agronomicIndicators = Agronomic_Indicator.objects.all()
            monitorings = Monitoring.objects.filter(greenhouse = greenhouse)
            for monitoring in monitorings:
                sensors = monitoring.sensors.all()
                
                for agronomicIndicator in agronomicIndicators:
                    indicators = agronomicIndicator.phys_vars.all()
                    addIndicator = True
                    for indicator in indicators:
                        if indicator not in sensors:
                            addIndicator = False
                    if addIndicator:
                        n = random.randint(15,50)
                        data['indicatorChart'+str(agronomicIndicator.id)] = n

                for sensor in sensors:             
                    n = random.randint(15,50)
                    data['sensorChart'+str(sensor.id)] = n
        return JsonResponse(data)