from django.contrib import admin
from main.models import Greenhouse, Station_Type, Crop, Physical_Variable, Monitoring, Variable_Type, Agronomic_Indicator, Greenhouse_Database_Connection, Crop_Limits

# Register your models here.
admin.site.register(Greenhouse)
admin.site.register(Crop)
admin.site.register(Monitoring)
admin.site.register(Variable_Type)
admin.site.register(Physical_Variable)
admin.site.register(Agronomic_Indicator)
admin.site.register(Station_Type)
admin.site.register(Greenhouse_Database_Connection)
admin.site.register(Crop_Limits)