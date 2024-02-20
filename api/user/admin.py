from django.contrib import admin
from .models import LdapUsers,Employee
# Register your models here.
admin.site.register(LdapUsers)
admin.site.register(Employee)

