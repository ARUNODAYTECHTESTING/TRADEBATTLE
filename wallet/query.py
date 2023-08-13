from wallet import models as wallet_models

def create_user_wallet(user):
    print(f"Execute wallet !! ->{user.id}")
    wallet, created = wallet_models.Wallet.objects.get_or_create(user=user)
    return wallet, created

def create_transaction(wallet,credit_type,action,amount):
    print("Transaction get execute")
    wallet_models.Transaction.objects.create(wallet=wallet,credit_type = credit_type,action = action,amount=amount)