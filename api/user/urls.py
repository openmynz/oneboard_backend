from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter, Route
from .views import EmployeeViewSet,LdapUsersViewSet,CustomEmployeeViewSet
router = DefaultRouter()

router.register(r"users", views.UserViewSet, basename="user-create")
router.register(r'employees',EmployeeViewSet)
router.register(r'ldap-users',LdapUsersViewSet)
router.register(r'employee-ldap-relationship',CustomEmployeeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
