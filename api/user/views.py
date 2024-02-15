from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
    BasicAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer,LdapUsersSerializer,EmployeeSerializer
from .models import Employee,LdapUsers

class UserViewSet(ModelViewSet):
    authentication_classes = [
        JWTAuthentication,
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        # Check if the requesting user is an admin
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # If the user is admin, proceed to retrieve and serialize all users
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Check if the requesting user is an admin
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Deserialize the incoming data
        serializer = self.get_serializer(data=request.data, many=True)

        # Validate the data
        if serializer.is_valid():
            # Save the validated data to create the users
            serializer.save()
            return Response(
                {"detail": "Users created successfully"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # Retrieve the user instance for the requested ID
        user = self.get_object()
        print(f"Requested user: {user}")
        print(f"Requesting user: {request.user}")

        # Check if the requesting user is the same as the requested user or is an admin
        if request.user == user or request.user.is_staff:
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, pk=None):
        # Retrieve the user instance for the requested ID
        user = self.get_object()

        # Check if the requesting user is the same as the requested user
        if request.user == user or request.user.is_staff:
            serializer = self.get_serializer(user, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"detail": "User updated successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def partial_update(self, request, pk=None):
        # Retrieve the user instance for the requested ID
        user = self.get_object()

        # Check if the requesting user is the same as the requested user or is admin
        if request.user == user or request.user.is_staff:
            serializer = self.get_serializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"detail": "User updated successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, pk=None):
        # Retrieve the user instance for the requested ID
        user = self.get_object()

        # Check if the requesting user is a superuser
        if request.user.is_superuser:
            # Delete the user
            user.delete()
            return Response(
                {"detail": "User deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        elif request.user.is_staff:
            # Admins cannot delete other admins
            if not user.is_staff:
                user.delete()
                return Response(
                    {"detail": "User deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"detail": "Admins cannot delete other admin users."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            # Regular users or admins trying to delete themselves
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(
        detail=True, methods=["POST", "OPTIONS"], permission_classes=[IsAuthenticated]
    )
    def change_password(self, request, pk=None):
        user = self.get_object()
        requesting_user = request.user

        # Check if the requesting user is a superuser or an admin
        if requesting_user.is_superuser or requesting_user.is_staff:
            # Superuser can change any password, admin can change non-admin password
            if user.is_superuser or not user.is_staff:
                password = request.data.get("password")
                if password:
                    user.set_password(password)
                    user.save()
                    return Response(
                        {"detail": "Password changed successfully"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail": "Admins cannot change passwords for other admin users."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        elif requesting_user == user:
            # Regular user can change their own password
            password = request.data.get("password")
            if password:
                user.set_password(password)
                user.save()
                return Response(
                    {"detail": "Password changed successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Regular user trying to change another user's password
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST", "OPTIONS"], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        print(request.headers)
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            # refresh.access_token.set_exp(timedelta(minutes=15))
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response(
                {
                    "detail": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Log out the currently authenticated user.
        Expected Output:
        - Status Code: 200 OK
        - Response: {'detail': 'Logout successful'}
        """
        user = request.user
        if user.is_authenticated:
            # Blacklist the refresh token to invalidate it
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                try:
                    RefreshToken(refresh_token).blacklist()
                except Exception:
                    return Response(
                        {"detail": "Invalid refresh token"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            logout(request)
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
class LdapUsersViewSet(ModelViewSet):
    queryset = LdapUsers.objects.all()
    serializer_class = LdapUsersSerializer

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer