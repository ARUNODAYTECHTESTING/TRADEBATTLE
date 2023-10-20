from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

def get_token(user_object):
    refresh = RefreshToken.for_user(user_object)
    token = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return token


class Conversion:
    @staticmethod
    def coin_to_rupees(coin: int):
        return int(coin) / 10

    @staticmethod
    def rupees_to_coin(rupees: int):
        return 10 * int(rupees)


# TODO: Common logic comes here
class DateTimeConversion:
    def str_datetime_into_datetime_obj(str_datetime: str) -> datetime:
        return datetime.strptime(str_datetime,"%Y%m%d:%H:%M:%S").date()