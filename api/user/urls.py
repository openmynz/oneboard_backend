from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    UserViewSet,
    EmployeeViewSet,
    LdapUsersViewSet,
    LdapUserEmployeeMappingAPIView,
)


router = DefaultRouter()

router.register(r"users", UserViewSet, basename="user-create")
router.register(r"employees", EmployeeViewSet)
router.register(r"ldap-users", LdapUsersViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "ldap-user-employee/",
        LdapUserEmployeeMappingAPIView.as_view(),
        name="ldap-user-employee",
    ),
]
