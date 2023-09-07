from django.test import TestCase
from shipments.serializers import AddressSerializer, ArticleSerializer, RetrieveShipmentSerializer
from shipments.models import Address, Shipment, Article, Carrier, Status, Location
from django_countries import countries

class AddressSerializerTestCase(TestCase):

    def test_valid_address_serializer(self):
        data = {
            'details': '123 Main St',
            'zipcode': '12345',
            'city': 'TestCity',
            'country': 'US',
        }
        serializer = AddressSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_address_serializer_output(self):
        location = Location.objects.create(lat=10.0, lon=20.0)
        address = Address.objects.create(details='123 Main St', zipcode='12345', city='TestCity', country='US', location=location)
        serializer = AddressSerializer(address)
        expected_data = {
            'id': address.id,
            'details': '123 Main St',
            'zipcode': '12345',
            'city': 'TestCity',
            'country': countries.name('US'),
            'location': location.id
        }
        self.assertEqual(serializer.data, expected_data)

class ArticleSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.carrier = Carrier.objects.create(name="TestCarrier")
        self.status = Status.objects.create(name="Delivered", order=1, description="Package delivered")
        self.location1 = Location.objects.create(lat=10.0, lon=20.0)
        self.address1 = Address.objects.create(details='123 Sender St', zipcode='12345', city='SenderCity', country='US', location=self.location1)
        self.location2 = Location.objects.create(lat=15.0, lon=25.0)
        self.address2 = Address.objects.create(details='123 Receiver St', zipcode='67890', city='ReceiverCity', country='US', location=self.location2)
        self.shipment = Shipment.objects.create(
            tracking_number="123456",
            carrier=self.carrier,
            sender_address=self.address1,
            receiver_address=self.address2,
            status=self.status
        )
        
    def test_valid_article_serializer(self):
        data = {
            'shipment': self.shipment.id,
            'name': 'Test Article',
            'quantity': 10,
            'price': 50.0,
            'sku': 'ABC123'
        }
        serializer = ArticleSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class ShipmentSerializerTestCase(TestCase):

    def setUp(self):
        self.carrier = Carrier.objects.create(name="TestCarrier")
        self.status = Status.objects.create(name="Delivered", order=1, description="Package delivered")
        self.location1 = Location.objects.create(lat=10.0, lon=20.0)
        self.address1 = Address.objects.create(details='123 Sender St', zipcode='12345', city='SenderCity', country='US', location=self.location1)
        self.location2 = Location.objects.create(lat=15.0, lon=25.0)
        self.address2 = Address.objects.create(details='123 Receiver St', zipcode='67890', city='ReceiverCity', country='US', location=self.location2)

    def test_valid_retrieve_shipment_serializer(self):
        shipment = Shipment.objects.create(
            tracking_number="123456",
            carrier=self.carrier,
            sender_address=self.address1,
            receiver_address=self.address2,
            status=self.status
        )
        Article.objects.create(shipment=shipment, name='Test Article', quantity=10, price=50.0, sku='ABC123')
        
        serializer = RetrieveShipmentSerializer(shipment)
        expected_sender_address = AddressSerializer(self.address1).data
        expected_receiver_address = AddressSerializer(self.address2).data
        expected_article = ArticleSerializer(Article.objects.first()).data
        
        self.assertEqual(serializer.data['sender_address'], expected_sender_address)
        self.assertEqual(serializer.data['receiver_address'], expected_receiver_address)
        self.assertEqual(serializer.data['articles'][0], expected_article)
