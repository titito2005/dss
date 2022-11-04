from nturl2path import url2pathname
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Crop(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Variable_Type(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Station_Type(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Physical_Variable(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    unit_of_measurement = models.CharField(max_length=15)
    type = models.ForeignKey(Variable_Type, on_delete=models.CASCADE, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def toJson(self):
        return {'name': self.name,
                'unit_of_measurement': self.unit_of_measurement,
                'type': self.type.name}

class Agronomic_Indicator(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    unit_of_measurement = models.CharField(max_length=15)
    phys_vars = models.ManyToManyField(Physical_Variable)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Greenhouse(models.Model):
    location = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=False)
    start_date = models.DateTimeField()
    def get_days_elapsed(self):
        return (timezone.now() - self.start_date).days
    def __str__(self):
        return str(self.owner) + " / " + self.location + " / " + str(self.crop) + " / " + str(self.start_date.strftime('%B %d %Y'))

class Monitoring(models.Model):
    greenhouse =  models.ForeignKey(Greenhouse, on_delete=models.CASCADE, null=False)
    type = models.ForeignKey(Station_Type, on_delete=models.CASCADE, null=False)
    sensors = models.ManyToManyField(Physical_Variable)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Greenhouse_Database_Connection(models.Model):
    greenhouse =  models.ForeignKey(Greenhouse, on_delete=models.CASCADE, null=False)
    url = models.CharField(max_length=300)
    ip = models.CharField(max_length=30)
    database_name = models.CharField(max_length=100)
    table_name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Crop_Limits(models.Model):
    class Meta:
        unique_together = ('crop', 'phys_vars'),
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=False)
    phys_vars = models.ForeignKey(Physical_Variable, on_delete=models.CASCADE, null=False)
    max_limit = models.CharField(max_length=20)
    min_limit = models.CharField(max_length=20)
