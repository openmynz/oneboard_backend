from django.shortcuts import render
from .models import Account,Project,User_Project_Mapping
from rest_framework import viewsets,status
from .serializers import AccountSerializer,ProjectSerializer,User_Project_MappingSerializer
from rest_framework.response import Response

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('account_id')
    serializer_class = AccountSerializer
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('project_id')
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        account_id = request.data.get('account_id')  # Get account_id from request data
        if not account_id:
            return Response({'error': 'account_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(account_id=account_id)
        except Account.DoesNotExist:
            return Response({'error': 'Invalid account_id'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class UserProjectMappingViewSet(viewsets.ModelViewSet):
    queryset = User_Project_Mapping.objects.all()
    serializer_class = User_Project_MappingSerializer
    