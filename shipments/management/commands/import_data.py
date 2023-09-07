import csv
from django.core.management.base import BaseCommand
from shipments.models import Carrier, Status, Shipment, Article, Address
from django_countries import countries

def country_code(country_name):
    for code, name in list(countries):
        if name == country_name:
            return code
    return ''

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **kwargs):
        
        confirmation = input("Are you sure you want to delete all data from the database? (y/n): ")
        if confirmation.lower() != 'y':
            print("Aborting operation.")
            return
        
        # delete all data from database
        Article.objects.all().delete()
        Shipment.objects.all().delete()
        Carrier.objects.all().delete()
        Status.objects.all().delete()
        Address.objects.all().delete()
        
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if Shipment.objects.filter(tracking_number=row['tracking_number']).exists():
                    shipment = Shipment.objects.get(tracking_number=row['tracking_number'])
                else:
                    rec_address_row = row['receiver_address']
                    det, zip_code_city, country = rec_address_row.split(',')
                    zip_code, city = zip_code_city.strip().split(' ')
                    rec_address, _ = Address.objects.get_or_create(
                        details=det,
                        zipcode=zip_code,
                        city=city,
                        country=country_code(country.strip())
                    )
                    send_address_row = row['sender_address']
                    det, zip_code_city, country = send_address_row.split(',')
                    zip_code, city = zip_code_city.strip().split(' ')
                    send_address, _ = Address.objects.get_or_create(
                        details=det,
                        zipcode=zip_code,
                        city=city,
                        country=country_code(country.strip())
                    )
                    carrier, _ = Carrier.objects.get_or_create(name=row['carrier'])
                    status, _ = Status.objects.get_or_create(name=row['status'], order=0)
                    shipment = Shipment.objects.create(
                        tracking_number=row['tracking_number'],
                        carrier=carrier,
                        sender_address=send_address,
                        receiver_address=rec_address,
                        status=status
                    )
                Article.objects.create(
                    shipment=shipment,
                    name=row['article_name'],
                    quantity=row['article_quantity'],
                    price=row['article_price'],
                    sku=row['SKU']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))