from rest_framework import serializers
from .models import Account,Project,User_Project_Mapping
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_id','account_name']
        read_only_fields = ['account_id']
class ProjectSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account_id.account_name', read_only=True)
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'account_id', 'account_name']
        read_only_fields = ['project_id']
class User_Project_MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_Project_Mapping
        fields = '__all__'

