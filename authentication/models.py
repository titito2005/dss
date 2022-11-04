from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
    def __str__(self):
        return self.name
class User_Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    changed_password = models.BooleanField(default = False)