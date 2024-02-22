# serializers.py
from .models import LdapUsers, Employee
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LdapUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LdapUsers
        fields = "__all__"

    def create(self, validated_data):
        employee_data = validated_data.pop("employee", {})
        ldap_user = LdapUsers.objects.create(**validated_data)
        Employee.objects.create(ldap_user=ldap_user, **employee_data)
        return ldap_user


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class LdapUserEmployeeSerializer(serializers.Serializer):
    ldap_user_id = serializers.IntegerField()
    employee_table_id = serializers.IntegerField(allow_null=True)
    common_name = serializers.CharField()
    account_name = serializers.CharField()
    employee_id = serializers.IntegerField(allow_null=True)
    email_id = serializers.EmailField(allow_blank=True, allow_null=True)
