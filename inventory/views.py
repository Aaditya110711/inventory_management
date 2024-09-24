import logging
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from inventory.models import InventoryItem
from inventory.serializers import InventoryItemSerializer

logger = logging.getLogger(__name__)


class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling InventoryItem CRUD operations.
    Implements Redis caching for the 'retrieve' action to optimize performance.
    All endpoints require authentication.
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new InventoryItem.
        Validates that the item name is unique before saving.
        Logs both successful creations and attempts to create duplicate items.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_name = serializer.validated_data['name']

        if InventoryItem.objects.filter(name=item_name).exists():
            logger.warning(f"Attempt to create duplicate item: {item_name}")
            raise ValidationError({"detail": "Item already exists."})

        self.perform_create(serializer)
        logger.info(f"Created new item: {serializer.data['name']}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an InventoryItem by ID.
        Uses Redis caching to optimize subsequent read operations.
        Logs cache hits and cache misses.
        """
        instance = self.get_object()
        cache_key = f'inventory_item_{instance.id}'

        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(
                f"Cache hit: Retrieved item '{instance.name}' from cache.")
            return Response(cached_data, status=status.HTTP_200_OK)

        # Cache miss - serialize and cache the data
        serializer = self.get_serializer(instance)
        cache.set(cache_key, serializer.data,
                  timeout=300)  
        logger.info(
            f"Cache miss: Retrieved item '{instance.name}' from database and cached it.")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update an InventoryItem.
        Clears the cache for the updated item after successful modification.
        Supports both full and partial updates.
        Logs successful updates and cache invalidations.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        cache_key = f'inventory_item_{instance.id}'
        cache.delete(cache_key)  

        logger.info(f"Updated item '{instance.name}'. Cache invalidated.")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an InventoryItem.
        Clears the cache for the deleted item.
        Logs successful deletions and cache invalidations.
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        cache_key = f'inventory_item_{instance.id}'
        cache.delete(cache_key)

        logger.info(f"Deleted item '{instance.name}'. Cache invalidated.")
        return Response(status=status.HTTP_204_NO_CONTENT)
