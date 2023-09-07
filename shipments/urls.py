from django.urls import path
from rest_framework import routers
from .views import ShipmentRetrieveView, ShipmentListView

urlpatterns = [
    path('shipments/', ShipmentListView.as_view(), name='shipment-list'),
    path('shipments/<str:carrier>/<str:tracking_number>/', ShipmentRetrieveView.as_view(), name='shipment-detail'),
]