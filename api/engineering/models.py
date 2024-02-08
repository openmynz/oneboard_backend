from django.db import models
from django.contrib.auth.models import User
class Account(models.Model):
    account_id = models.CharField(primary_key=True,max_length=20)
    account_name = models.CharField(max_length=50)
class Project(models.Model):
    project_id = models.CharField(primary_key=True,max_length=20)
    account_id = models.ForeignKey(Account,on_delete = models.CASCADE)
    project_name = models.CharField(max_length=50)

class User_Project_Mapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Project_id = models.ForeignKey(Project, on_delete=models.CASCADE)