from django.contrib import admin
from .models import Carrier, Status, Shipment, Article, Address

@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'description')

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'carrier', 'sender_address', 'receiver_address', 'status')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'name', 'quantity', 'price', 'sku')
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('details', 'zipcode', 'city', 'country')