from django.db import IntegrityError
from django.test import TestCase
from django_countries import countries
from ..models import Carrier, Status, Address, Shipment, Article

class CarrierModelTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name='Test Carrier')

    def test_carrier_fields(self):
        self.assertEqual(self.carrier.name, 'Test Carrier')

class StatusModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name='Test Status', order=1, description='Test Description')

    def test_status_fields(self):
        self.assertEqual(self.status.name, 'Test Status')
        self.assertEqual(self.status.order, 1)
        self.assertEqual(self.status.description, 'Test Description')

class AddressModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(details='Test Address', zipcode='12345', city='Test City', country=countries[0][0])

    def test_address_fields(self):
        self.assertEqual(self.address.details, 'Test Address')
        self.assertEqual(self.address.zipcode, '12345')
        self.assertEqual(self.address.city, 'Test City')
        self.assertEqual(self.address.country, countries[0][0])

class ShipmentModelTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name='Test Carrier')
        self.sender_address = Address.objects.create(details='Test Sender Address', zipcode='12345', city='Test City', country=countries[0][0])
        self.receiver_address = Address.objects.create(details='Test Receiver Address', zipcode='54321', city='Test City', country=countries[1][0])
        self.status = Status.objects.create(name='Test Status', order=1, description='Test Description')
        self.shipment = Shipment.objects.create(tracking_number='1234567890', carrier=self.carrier, sender_address=self.sender_address, receiver_address=self.receiver_address, status=self.status)

    def test_shipment_fields(self):
        self.assertEqual(self.shipment.tracking_number, '1234567890')
        self.assertEqual(self.shipment.carrier, self.carrier)
        self.assertEqual(self.shipment.sender_address, self.sender_address)
        self.assertEqual(self.shipment.receiver_address, self.receiver_address)
        self.assertEqual(self.shipment.status, self.status)
        
    def test_shipment_unique_together(self):
        with self.assertRaises(Exception) as raised:
            Shipment.objects.create(tracking_number='1234567890', carrier=self.carrier, sender_address=self.sender_address, receiver_address=self.receiver_address, status=self.status)
        self.assertEqual(IntegrityError, type(raised.exception))

class ArticleModelTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name='Test Carrier')
        self.sender_address = Address.objects.create(details='Test Sender Address', zipcode='12345', city='Test City', country=countries[0][0])
        self.receiver_address = Address.objects.create(details='Test Receiver Address', zipcode='54321', city='Test City', country=countries[1][0])
        self.status = Status.objects.create(name='Test Status', order=1, description='Test Description')
        self.shipment = Shipment.objects.create(tracking_number='1234567890', carrier=self.carrier, sender_address=self.sender_address, receiver_address=self.receiver_address, status=self.status)
        self.article = Article.objects.create(shipment=self.shipment, name='Test Article', quantity=1, price=1.0, sku='12345')

    def test_article_fields(self):
        self.assertEqual(self.article.shipment, self.shipment)
        self.assertEqual(self.article.name, 'Test Article')
        self.assertEqual(self.article.quantity, 1)
        self.assertEqual(self.article.price, 1.0)
        self.assertEqual(self.article.sku, '12345')
        
    def test_article_unique_together(self):
        with self.assertRaises(Exception) as raised:
            Article.objects.create(shipment=self.shipment, name='Test Article', quantity=1, price=1.0, sku='12345')
        self.assertEqual(IntegrityError, type(raised.exception))