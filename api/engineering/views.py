from django.shortcuts import render
from .models import Account,Project,User_Project_Mapping
from rest_framework import viewsets
from .serializers import AccountSerializer,ProjectSerializer,User_Project_MappingSerializer

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
class UserProjectMappingViewSet(viewsets.ModelViewSet):
    queryset = User_Project_Mapping.objects.all()
    serializer_class = User_Project_MappingSerializer
    