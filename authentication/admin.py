from django.contrib import admin
from authentication.models import Role, User_Role

# Register your models here.
admin.site.register(Role)
admin.site.register(User_Role)