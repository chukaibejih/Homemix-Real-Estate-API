from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from .models import Property
from .views import CustomPageNumberPagination


class PropertyViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test2@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            role='seller', # if you are testing for create property or anything that involves a seller, set this filed correctly
            referral_code='HM-4UKCzY',
            is_verified=True
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('properties-list')

        
        self.property_1 = Property.objects.create(
            seller=self.user,
            address="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="12345",
            property_type="Residential Property",
            price="100000.00",
            beds=3,
            baths=2,
            description="This is a beautiful home.",
            image_urls="http://example.com/image1.jpg",
            posted="2022-01-01T00:00:00Z",
            status="available"
        )
        self.property_2 = Property.objects.create(
            seller=self.user,
            address="456 Elm St",
            city="Anytown",
            state="CA",
            zip_code="12345",
            property_type="Commercial Property",
            price="500000.00",
            beds=0,
            baths=0,
            description="This is a great commercial property.",
            image_urls="http://example.com/image2.jpg",
            posted="2022-01-01T00:00:00Z",
            status="available"
        )
        self.url = reverse('properties-list')
        self.pagination = CustomPageNumberPagination()

    def test_list_properties(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_search_properties(self):
        query_params = {
            'search': 'commercial',
        }
        response = self.client.get(self.url, query_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], str(self.property_2.id))

    def test_throttle_properties(self):
        for i in range(31):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_unauthorized_request(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_property(self):
        data = {
            "address": "123 Test St",
            "city": "Test City",
            "state": "Test State",
            "zip_code": "12345",
            "property_type": "residential property",
            "price": 100000,
            "beds": 3,
            "baths": 2,
            "description": "Test description",
            "image_urls": "https://example.com/test.jpg",
            "status": "available"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 3)

    def test_retrieve_property(self):
        property_id = self.property_1.id
        response = self.client.get(reverse('properties-detail', kwargs={'pk': property_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(property_id))
        self.assertEqual(response.data['address'], self.property_1.address)    

    def test_delete_property(self):
        property_id = self.property_1.id
        response = self.client.delete(reverse('properties-detail', kwargs={'pk': property_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Property.objects.filter(id=property_id).exists())

    def test_unauthorized_create_property(self):
        self.client.force_authenticate(user=None)
        data = {
            'seller': self.user.id,
            'address': '789 Oak St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '12345',
            'property_type': 'Residential Property',
            'price': '200000.00',
            'beds': 4,
            'baths': 2,
            'description': 'This is another beautiful home.',
            'image_urls': 'http://example.com/image3.jpg',
            'status': Property.Status.AVAILABLE
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





