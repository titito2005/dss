from django import template
from django.urls import path
from django.urls.base import reverse_lazy

#Local views
from .views import AddCropsView, AddGreenhouseView, AddLimitView, AddMonitoringView, AgronomicIndicatorView, EditLimitView
from .views import ConfigGreenhouseView, CropsView, DataView, DeleteCropView 
from .views import DeleteGreenhouseView, DeleteIndicatorView, DeleteMonitoringView, DeletePhysicalVarView 
from .views import EditGreenhouseView, EditIndicatorView, EditMonitoringView, GreenhouseDetailsView, LimitsView
from .views import GreenhousesView, HomeView, MonitoringView, PhysVarView, EditCropView, EditPhysicalVarView
from .views import AddPhysicalVarView, AddIndicatorView, MonitoringsView, GreenhouseDataView, DeleteLimitView


#namespace
app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    #Monitorings paths
    path('monitoring/', MonitoringView.as_view(), name="monitoring"),
    path('monitorings/', MonitoringsView.as_view(), name="monitorings"),
    path('add_monitoring/', AddMonitoringView.as_view(), name="add_monitoring"),
    path('edit_monitoring/<int:id>/', EditMonitoringView.as_view(), name="edit_monitoring"),
    path('delete_monitoring/<int:id>/', DeleteMonitoringView.as_view(), name="delete_monitoring"),
    #Physical variable paths
    path('physical_variable/', PhysVarView.as_view(), name="phys_var"),
    path('add_physical_variable/', AddPhysicalVarView.as_view(), name="add_phys_var"),
    path('add_physical_variable/<int:id>/', EditPhysicalVarView.as_view(), name="edit_phys_var"),
    path('delete_physical_variable/<int:id>/', DeletePhysicalVarView.as_view(), name="delete_phys_var"),
    #Agronomic indicator paths
    path('agronomic_indicator/', AgronomicIndicatorView.as_view(), name="indicator"),
    path('add_indicator/', AddIndicatorView.as_view(), name="add_indicator"),
    path('edit_indicator/<int:id>/', EditIndicatorView.as_view(), name="edit_indicator"),
    path('delete_indicator/<int:id>/', DeleteIndicatorView.as_view(), name="delete_indicator"),
    #Greenhouses paths
    path('greenhouses/', GreenhousesView.as_view(), name="greenhouses"),
    path('add_greenhouse/', AddGreenhouseView.as_view(), name="add_greenhouse"),
    path('greenhouses/details/<int:id>/', GreenhouseDetailsView.as_view(), name="greenhouse_details"),
    path('edit_greenhouse/<int:id>/', EditGreenhouseView.as_view(), name="edit_greenhouse"),
    path('delete_greenhouse/<int:id>/', DeleteGreenhouseView.as_view(), name="delete_greenhouse"),
    path('greenhouse_data/<int:id>/', GreenhouseDataView.as_view(), name="greenhouse_data"),
    path('config_greenhouse/<int:id>/', ConfigGreenhouseView.as_view(), name="config_greenhouse"),
    #Crops paths
    path('crops/', CropsView.as_view(), name="crops"),
    path('add_crop/', AddCropsView.as_view(), name="add_crops"),
    path('edit_crop/<int:id>/', EditCropView.as_view(), name="edit_crops"),
    path('delete_crop/<int:id>/', DeleteCropView.as_view(), name='delete_crop'),

    #Limit paths
    path('limits/', LimitsView.as_view(), name="limits"),
    path('add_limit/', AddLimitView.as_view(), name="add_limit"),
    path('edit_limit/<int:id>/', EditLimitView.as_view(), name="edit_limit"),
    path('delete_limit/<int:id>/', DeleteLimitView.as_view(), name='delete_limit'),

    #charts data paths
    path('data/<int:id>/', DataView.as_view(), name='char_data'),
]
