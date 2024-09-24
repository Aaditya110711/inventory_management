from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import InventoryItem

class InventoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.item = InventoryItem.objects.create(name='Test Item', description='Test Description', quantity=10)

    def test_create_item(self):
        url = reverse('inventoryitem-list')
        data = {'name': 'New Item', 'description': 'New Description', 'quantity': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 2)
        self.assertEqual(InventoryItem.objects.get(name='New Item').description, 'New Description')

    def test_retrieve_item(self):
        url = reverse('inventoryitem-detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)