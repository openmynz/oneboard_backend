from django.contrib import admin
from .models import  Project,Account,User_Project_Mapping
# Register your models here.
admin.site.register(Account)
admin.site.register(Project)
admin.site.register(User_Project_Mapping)