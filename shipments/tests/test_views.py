from django.test import TestCase, RequestFactory
from unittest.mock import patch
from shipments.models import Shipment, Carrier, Status, Address
from shipments.views import ShipmentRetrieveView, ShipmentListView
from django.urls import reverse

class ShipmentRetrieveViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.carrier = Carrier.objects.create(name="TestCarrier")
        self.status = Status.objects.create(name="Shipped", order=1, description="Test description")
        self.sender_address = Address.objects.create(details="Sender Detail", zipcode="12345", city="CityA", country="US")
        self.receiver_address = Address.objects.create(details="Receiver Detail", zipcode="67890", city="CityB", country="CA")
        self.shipment = Shipment.objects.create(tracking_number="1234567890", carrier=self.carrier, sender_address=self.sender_address, receiver_address=self.receiver_address, status=self.status)

    @patch('shipments.views.geocoding_to_weather_cache')
    def test_retrieve_shipment(self, mock_geocoding):
        mock_geocoding.return_value = {"weather": "sunny"}
        
        carrier_name = "TestCarrier"
        tracking_number = "1234567890"
        url = reverse('shipment-detail', kwargs={'carrier': carrier_name, 'tracking_number': tracking_number})
        request = self.factory.get(url)
        response = ShipmentRetrieveView.as_view()(request, carrier=carrier_name, tracking_number=tracking_number)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['tracking_number'], "1234567890")
        self.assertEqual(response.data['weather'], {"weather": "sunny"})

    def test_retrieve_shipment_not_found(self):
        carrier_name = "TestCarrier"
        tracking_number = "noneexistent"
        url = reverse('shipment-detail', kwargs={'carrier': carrier_name, 'tracking_number': tracking_number})
        request = self.factory.get(url)
        response = ShipmentRetrieveView.as_view()(request, carrier=carrier_name, tracking_number=tracking_number)
        self.assertEqual(response.status_code, 404)

class ShipmentListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = ShipmentListView.as_view()
        # Dummy data for testing
        self.carrier = Carrier.objects.create(name="TestCarrier")
        self.status = Status.objects.create(name="Shipped", order=1, description="Test description")
        self.sender_address = Address.objects.create(details="Sender Detail", zipcode="12345", city="CityA", country="US")
        self.receiver_address = Address.objects.create(details="Receiver Detail", zipcode="67890", city="CityB", country="CA")
        self.shipment = Shipment.objects.create(tracking_number="1234567890", carrier=self.carrier, sender_address=self.sender_address, receiver_address=self.receiver_address, status=self.status)

    def test_list_shipment(self):
        request = self.factory.get('/shipments/')
        response = self.view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['tracking_number'], "1234567890")