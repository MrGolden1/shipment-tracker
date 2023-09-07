from django.db import models
from django_countries.fields import CountryField

from django.db import models


class Carrier(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)
    
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order = models.IntegerField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    
    def __str__(self):
        return str(f"{self.lat}, {self.lon}")

class AddressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('location')
    
class Address(models.Model):
    details = models.TextField()
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = CountryField()
    location = models.OneToOneField(Location, blank=True, null=True,on_delete=models.SET_NULL)

    objects = AddressManager()
    
    def __str__(self):
        return str(f"{self.details}, {self.zipcode}, {self.city}, {self.country}")

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=50, db_index=True)
    carrier = models.ForeignKey(Carrier, on_delete=models.PROTECT)
    sender_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='shipments_sent')
    receiver_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='shipments_received')
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.tracking_number)
    
    class Meta:
        unique_together = ('tracking_number', 'carrier')
    
class Article(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.PROTECT, related_name='articles')
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()
    sku = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        unique_together = ('shipment', 'sku')