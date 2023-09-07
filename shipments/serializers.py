from rest_framework import serializers
from .models import Shipment, Article, Address


class AddressSerializer(serializers.ModelSerializer):
    # country name instead of country code
    country = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = Address
        fields = '__all__'
    
    
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ListShipmentSerializer(serializers.ModelSerializer):
    sender_address = AddressSerializer()
    receiver_address = AddressSerializer()
    carrier = serializers.CharField(source='carrier.name', read_only=True)
    status = serializers.CharField(source='status.name', read_only=True)
    
    class Meta:
        model = Shipment
        fields = ['id', 'tracking_number', 'sender_address', 'receiver_address', 'status', 'carrier']

class RetrieveShipmentSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)
    sender_address = AddressSerializer()
    receiver_address = AddressSerializer()
    status = serializers.CharField(source='status.name', read_only=True)
    carrier = serializers.CharField(source='carrier.name', read_only=True)
    
    class Meta:
        model = Shipment
        fields = '__all__'
