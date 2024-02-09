from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Employee(models.Model):
    employee_id = models.CharField(primary_key=True,max_length=20)
    employee_name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    joining_date = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=40)
    contact_no = models.CharField(max_length=10)    
    blood_group = models.CharField(max_length=20)  
    manager = models.CharField(max_length=30)

    