from rest_framework import serializers
from .models import Account,Project,User_Project_Mapping
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'
class User_Project_MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_Project_Mapping
        fields = '__all__'

