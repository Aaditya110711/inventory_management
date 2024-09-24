from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import InventoryItemViewSet

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]