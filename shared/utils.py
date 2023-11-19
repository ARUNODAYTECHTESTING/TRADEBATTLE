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
    
    @staticmethod
    def datetime_obj_into_str_datetime(datetime_obj):
        return datetime_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')
    


from datetime import timedelta
class Entry:


    def sum_time_durations(time):
        list_of_time = [item for sublist in time for item in sublist]

        total_duration = timedelta()

        for time_str in list_of_time:
            time_parts = time_str.split(':')
            if len(time_parts) == 3:
                hours, minutes, seconds = map(int, time_parts)
            else:
                hours, minutes, seconds = 0, int(time_parts[0]), 0

            total_duration += timedelta(hours=hours, minutes=minutes, seconds=seconds)

        total_seconds = total_duration.total_seconds()
        total_hours, remainder = divmod(total_seconds, 3600)
        total_minutes, total_seconds = divmod(remainder, 60)

        total_time_str = f"{int(total_hours):02}:{int(total_minutes):02}:{int(total_seconds):02}"
        return total_time_str


    @staticmethod
    def get_user_time(entry: dict):
        list_of_time = []
        for key,val in entry.items():
            list_of_time.append(list(val[0].values()))
        return Entry.sum_time_durations(list_of_time)
    @staticmethod
    def find_average_time(entries: dict):
        list_of_time = []
        for entry in entries:
            for counter, (key, val) in enumerate(entry[0].items()):
                list_of_time.append(list(val[0].values()))
            list_of_time = [item for sublist in list_of_time for item in sublist]

            total_duration = timedelta()
            for time_str in list_of_time:
                time_parts = time_str.split(':')
                if len(time_parts) == 3:
                    hours, minutes, seconds = map(int, time_parts)
                else:
                    hours, minutes, seconds = 0, int(time_parts[0]), 0

                total_duration += timedelta(hours=hours, minutes=minutes, seconds=seconds)

            total_seconds = total_duration.total_seconds()
            total_hours, remainder = divmod(total_seconds, 3600)
            total_minutes, total_seconds = divmod(remainder, 60)

            total_time_str = f"{int(total_hours):02}:{int(total_minutes):02}:{int(total_seconds):02}"
            print(total_time_str)
            breakpoint()
            print(total_time_str/100*counter)
            list_of_time = []
            breakpoint()
        