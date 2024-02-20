from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, ProjectViewSet, UserProjectMappingViewSet

router = DefaultRouter()
router.register(r"clientaccounts", AccountViewSet)
router.register(r"projects", ProjectViewSet)
router.register(r"user-project-mappings", UserProjectMappingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
