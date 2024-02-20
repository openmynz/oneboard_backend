# serializers.py
from .models import LdapUsers,Employee
from rest_framework import serializers
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class LdapUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LdapUsers
        fields = '__all__'
class EmployeeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='ldap_user.first_name',read_only = True)
    account_name = serializers.CharField(source='ldap_user.account_name',read_only = True)
    last_name = serializers.CharField(source='ldap_user.last_name',read_only = True)
    
    class Meta:
        model = Employee
        fields = '__all__'
        # ['first_name','account_name','last_name','BLOOD_GROUPS','ROLE_CHOICES','employee_id','joining_date','ldap_user','reports_to','contact_number','emergency_contact_number','email_id','role','blood_group','profile_photo']
        read_only_fields = ['first_name','account_name','last_name']




        