from django.core.management.base import BaseCommand
from django.utils import timezone
from battles.models import StockData
from battles.stock_data import get_stock_data

class Command(BaseCommand):
    help = 'Update stock data in the database'

    def handle(self, *args, **options):
        stock_data_list = get_stock_data()

        if 'error' in stock_data_list:
            self.stdout.write(self.style.ERROR(f"Error fetching stock data: {stock_data_list['error']}"))
            return

        for stock_data in stock_data_list:
            symbol = stock_data['symbol']
            last_update_time = timezone.datetime.strptime(stock_data['lastUpdateTime'], "%d-%b-%Y %H:%M:%S")

            if any(value == "-" for value in stock_data.values()):
                self.stdout.write(self.style.WARNING(f"Skipping stock data with blank values for symbol: {symbol}"))
                continue
            # Check if data with the same symbol already exists
            existing_data = StockData.objects.filter(symbol=symbol).first()

            if existing_data:
                # Update existing entry
                existing_data.identifier = stock_data['identifier']
                existing_data.open_price = stock_data['open']
                existing_data.day_high = stock_data['dayHigh']
                existing_data.day_low = stock_data['dayLow']
                existing_data.last_price = stock_data['lastPrice']
                existing_data.previous_close = stock_data['previousClose']
                existing_data.change = stock_data['change']
                existing_data.p_change = stock_data['pChange']
                existing_data.year_high = stock_data['yearHigh']
                existing_data.year_low = stock_data['yearLow']
                existing_data.total_traded_volume = stock_data['totalTradedVolume']
                existing_data.total_traded_value = stock_data['totalTradedValue']
                existing_data.last_update_time = last_update_time
                existing_data.per_change_365d = stock_data['perChange365d']
                existing_data.per_change_30d = stock_data['perChange30d']
                existing_data.save()
                self.stdout.write(self.style.SUCCESS(f"Updated stock data for symbol: {symbol}"))
            else:
                # Create a new entry
                StockData.objects.create(
                    symbol=symbol,
                    identifier=stock_data['identifier'],
                    open_price=stock_data['open'],
                    day_high=stock_data['dayHigh'],
                    day_low=stock_data['dayLow'],
                    last_price=stock_data['lastPrice'],
                    previous_close=stock_data['previousClose'],
                    change=stock_data['change'],
                    p_change=stock_data['pChange'],
                    year_high=stock_data['yearHigh'],
                    year_low=stock_data['yearLow'],
                    total_traded_volume=stock_data['totalTradedVolume'],
                    total_traded_value=stock_data['totalTradedValue'],
                    last_update_time=last_update_time,
                    per_change_365d=stock_data['perChange365d'],
                    per_change_30d=stock_data['perChange30d']
                )
                self.stdout.write(self.style.SUCCESS(f"Created new stock data for symbol: {symbol}"))
