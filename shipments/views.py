from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Shipment
from .serializers import RetrieveShipmentSerializer, ListShipmentSerializer
from .tasks.owm import geocoding_to_weather_cache
from rest_framework import pagination

class ShipmentRetrieveView(APIView):
    
    def get_queryset(self):
        return Shipment.objects.select_related(
            'status', 'carrier', 'sender_address', 'receiver_address').prefetch_related('articles')

    def get(self, request, carrier, tracking_number):

        shipment = get_object_or_404(
            self.get_queryset(), tracking_number=tracking_number, carrier__name=carrier)
        
        
        data = RetrieveShipmentSerializer(shipment).data
        
        try:
            weather = geocoding_to_weather_cache(shipment.receiver_address.pk)
            data['weather'] = weather
        except:
            data['weather'] = None
            
        return Response(data)

class ShipmentPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class ShipmentListView(ListAPIView):
    
    pagination_class = ShipmentPagination

    queryset = Shipment.objects.select_related(
        'status', 'carrier', 'sender_address', 'receiver_address')

    serializer_class = ListShipmentSerializer
