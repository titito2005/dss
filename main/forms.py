from django import forms
from main.models import Crop, Greenhouse, Physical_Variable, Station_Type, Variable_Type

class AddGreenHouseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        userId = kwargs.pop('id')
        super(AddGreenHouseForm, self).__init__(*args, **kwargs)
        if(userId != 0):
            self.fields['crop'] = forms.ModelChoiceField(
                required=True,
                queryset=Crop.objects.filter(created_by = userId),
                initial= 0,
                widget=forms.Select(attrs={
                    'class': 'drop-button',}))
        else:
            self.fields['crop'] = forms.ModelChoiceField(
                required=True,
                queryset=Crop.objects.all(),
                initial= 0,
                widget=forms.Select(attrs={
                    'class': 'drop-button',}))

    location = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese la ubicación donde se encuentra el invernadero'}))

    owner = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese el nombre del encargado'}))

    start_date = forms.DateTimeField(
        required=True,
        input_formats=['%I:%M %p %d-%m-%Y'],
        widget = forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'input-text' },
            format='%I:%M %p %d-%m-%Y'))

class EditGreenHouseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        userId = kwargs.pop('id')
        super(EditGreenHouseForm, self).__init__(*args, **kwargs)
        if(userId != 0):
            self.fields['crop'] = forms.ModelChoiceField(
                required=True,
                queryset=Crop.objects.filter(created_by = userId),
                initial= 0,
                widget=forms.Select(attrs={
                    'class': 'drop-button',}))
        else:
            self.fields['crop'] = forms.ModelChoiceField(
                required=True,
                queryset=Crop.objects.all(),
                initial= 0,
                widget=forms.Select(attrs={
                    'class': 'drop-button',}))

    greenhouse_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
             'readonly': ''}))

    location = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese la ubicación donde se encuentra el invernadero'}))

    owner = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese el nombre del encargado'}))

    start_date = forms.DateTimeField(
        required=True,
        input_formats=['%I:%M %p %d-%m-%Y'],
        widget = forms.DateTimeInput(attrs={
            'class': 'input-text' },
            format='%I:%M %p %d-%m-%Y'))

class AddMonitoringForm(forms.Form):
    def __init__(self, *args, **kwargs):
        userId = kwargs.pop('id')
        super(AddMonitoringForm, self).__init__(*args, **kwargs)
        if(userId != 0):
            self.fields['greenhouse'] = forms.ModelChoiceField(
                required = True,
                queryset=Greenhouse.objects.filter(created_by = userId),
                initial= 0,
                widget=forms.Select(attrs={
                    'class': 'drop-button',}))

            self.fields['variables'] = forms.ModelMultipleChoiceField(
                queryset=Physical_Variable.objects.all(),
                widget=forms.CheckboxSelectMultiple)
        else:
            self.fields['greenhouse'] = forms.ModelChoiceField(
                required = True,
                queryset=Greenhouse.objects.all(),
                initial= 0,
                widget=forms.Select(attrs={
                    'class': 'drop-button',}))

            self.fields['variables'] = forms.ModelMultipleChoiceField(
                queryset=Physical_Variable.objects.all(),
                widget=forms.CheckboxSelectMultiple)

    type = forms.ModelChoiceField(
        required=True,
        queryset=Station_Type.objects.all(),
        initial= 0,
        widget=forms.Select(attrs={
            'class': 'drop-button'}))


class EditMonitoringForm(AddMonitoringForm):
    monitoring_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
             'readonly': ''}))

class AddPhysicalVarForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese el nombre de la variable física'}))

    description = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese una breve descripción de la variable física'}))

    unit_of_measurement = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese la unidad de medida que utiliza la variable física'}))

    type = forms.ModelChoiceField(
        required=True,
        queryset=Variable_Type.objects.all(),
        initial= 0,
        widget=forms.Select(attrs={
            'class': 'drop-button'}))

class EditPhysicalVarForm(AddPhysicalVarForm):
    physical_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
             'readonly': ''}))

class GreenHouseConfigForm(forms.Form):
    greenhouse =  forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
             'readonly': ''}))
    url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-text'}))
    ip = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-text'}))
    database_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-text'}))
    table_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-text'}))
    user = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-text'}))
    password = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-text'}))

class AddIndicatorForm(forms.Form):
    def __init__(self, *args, **kwargs):
        userId = kwargs.pop('id')
        super(AddIndicatorForm, self).__init__(*args, **kwargs)
        if(userId != 0):
            self.fields['variables'] = forms.ModelMultipleChoiceField(
                queryset=Physical_Variable.objects.filter(created_by = userId),
                widget=forms.CheckboxSelectMultiple)
        else:
            self.fields['variables'] = forms.ModelMultipleChoiceField(
                queryset=Physical_Variable.objects.all(),
                widget=forms.CheckboxSelectMultiple)

    name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese el nombre del indicador agronómico'}))

    description = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese una breve descripción del indicador agronómico'}))

    unit_of_measurement = forms.CharField(
            required=True,
            max_length=100,
            widget=forms.TextInput(attrs={
                'class': 'input-text',
                'placeholder': 'Ingrese la unidad de medida que utiliza el indicador agronómico'}))

class EditIndicatorForm(AddIndicatorForm):
    indicator_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
             'readonly': ''}))

class AddCropForm(forms.Form):
    name = forms.CharField(
        required= True,
        max_length=100,
        widget=forms.TextInput(attrs={
                'class': 'input-text',
                'placeholder': 'Ingrese el nombre del cultivo'}))

    description = forms.CharField(
        required= True,
        max_length=100,
        widget=forms.TextInput(attrs={
                'class': 'input-text',
                'placeholder': 'Ingrese la descripción del cultivo'}))

class EditCropForm(AddCropForm):
    crop_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
             'readonly': ''}))

class AddLimitForm(forms.Form):
    crop = forms.ModelChoiceField(
        required=True,
        queryset=Crop.objects.all(),
        initial= 0,
        widget=forms.Select(attrs={
            'class': 'drop-button'}))
    
    phys_vars = forms.ModelChoiceField(
        required=True,
        queryset=Physical_Variable.objects.all(),
        initial= 0,
        widget=forms.Select(attrs={
            'class': 'drop-button'}))
    
    max_limit = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese el valor máximo'}))
    
    min_limit = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
            'placeholder': 'Ingrese el valor mínimo'}))

class EditLimitForm(AddLimitForm):
    limit_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-text',
             'readonly': ''}))