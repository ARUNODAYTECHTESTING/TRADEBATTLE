from django.db import transaction
from .models import LeagueBattleUser, StockData

def update_stock_data_percentages():
    try:
        with transaction.atomic():
            # Dictionary to store the count of users who selected each stock
            stock_selection_count = set()

            # Iterate through all LeagueBattleUser instances
            for league_battle_user in LeagueBattleUser.objects.all():
                # Iterate through entries in submitted_time_and_answers
                for entry_key, entry_list in league_battle_user.submitted_time_and_answers.items():
                    # Check if the user has already selected a stock in this entry
                    entry_symbols = set()

                    # Iterate through each entry in the list
                    for entry in entry_list:
                        # Iterate through each symbol and percentage in the entry
                        for symbol, percent in entry.items():
                            symbol = symbol.lower()

                            if percent and percent[:-1].replace('.', '').isdigit():
                                percent = float(percent[:-1])

                                # Check if the user has already selected this stock in this entry
                                if symbol not in entry_symbols:
                                    entry_symbols.add(symbol)

                                    # Update the count of users who selected each stock
                                    stock_selection_count.add(symbol)

                                    # Update the selected_percent field in StockData
                                    stock_data = StockData.objects.filter(symbol__iexact=symbol).first()
                                    if stock_data:
                                        stock_data.selected_percent = len(stock_selection_count)
                                        stock_data.save()

    except Exception as e:
        print(f"Error updating stock data percentages: {e}")


