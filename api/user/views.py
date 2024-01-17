# views.py
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSet(ViewSet):
    permission_classes = [AllowAny]  # Adjust as needed
    serializer_class = UserSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def create(self, request):
        """
        Create a new user.

        Expected Input:
        - username: The desired username for the new user.
        - password: The password for the new user.

        Expected Output (Success):
        - Status Code: 201 Created
        - Response: {'detail': 'User created successfully'}

        Expected Output (Failure):
        - Status Code: 400 Bad Request
        - Response: {'detail': 'Invalid data'}
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        """
        Log in a user.

        Expected Input:
        - username: The username of the user.
        - password: The password of the user.

        Expected Output (Success):
        - Status Code: 200 OK
        - Response: {'detail': 'Login successful', 'access_token': '<token>'}

        Expected Output (Failure):
        - Status Code: 401 Unauthorized
        - Response: {'detail': 'Invalid credentials'}
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'detail': 'Login successful', 'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def logout(self, request):
        """
        Log out the currently authenticated user.

        Expected Output:
        - Status Code: 200 OK
        - Response: {'detail': 'Logout successful'}
        """
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

    def assign_group(self, request, pk=None):
        """
        Assign a user to a group.

        Expected Input:
        - group_name: The name of the group to assign the user to.

        Expected Output (Success):
        - Status Code: 200 OK
        - Response: {'detail': 'Group assigned successfully'}

        Expected Output (Failure):
        - Status Code: 404 Not Found
        - Response: {'detail': 'Group does not exist'}
        """
        user = get_object_or_404(User, pk=pk)
        group_name = request.data.get('group_name')

        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return Response({'detail': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user.groups.add(group)
        return Response({'detail': 'Group assigned successfully'}, status=status.HTTP_200_OK)
