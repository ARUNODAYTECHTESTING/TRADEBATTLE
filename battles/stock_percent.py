from collections import defaultdict

from battles.models import LeagueBattleUser

def calculate_stock_percentage_with_amount(max_stock):
    # Step 1: Retrieve all LeagueBattleUser instances
    all_users = LeagueBattleUser.objects.all()

    # Step 2-3: Extract selected stocks and amounts, and count occurrences
    stock_counter = defaultdict(float)
    total_users = len(all_users)

    for user in all_users:
        entries = user.submitted_time_and_answers.items()
        for entry_key, selected_stocks in entries:
            for stock in selected_stocks:
                symbol = stock["symbol"]
                amount = stock.get("amount", 1)  # Assuming default amount is 1 if not provided
                stock_counter[symbol] += amount

    # Step 4: Calculate percentage for each stock
    stock_percentages = {}

    for symbol, total_amount in stock_counter.items():
        percentage = (total_amount / (total_users * max_stock)) * 100  # Assuming 10 is the maximum amount a user can select
        stock_percentages[symbol] = percentage

    return stock_percentages


