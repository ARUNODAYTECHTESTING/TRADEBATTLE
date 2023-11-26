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

    @staticmethod
    def sum_list_of_times_into_str(list_of_time):
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
    def calculate_average_time(users_entry_average_sum,counter):
        # Convert total time to a timedelta object
        total_time_delta = datetime.strptime(users_entry_average_sum, "%H:%M:%S") - datetime(1900, 1, 1)

        # Convert total time to seconds
        total_seconds = total_time_delta.total_seconds()

        # Calculate average time per person 
        average_seconds = total_seconds / counter

        # Convert average back to timedelta
        average_timedelta = timedelta(seconds=average_seconds)

        # Format average as HH:MM:SS
        average_time_str = str(average_timedelta)  
        return average_time_str

    @staticmethod
    def sum_time_durations(time):
        list_of_time = [item for sublist in time for item in sublist]
        print(list_of_time)
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
        users_average_time = []
        per_user_entries = []
        for entry in entries:
            for counter, (key, val) in enumerate(entry[0].items()):
                per_user_entries.append(list(val[0].values()))
            per_user_average_time = Entry.sum_time_durations(per_user_entries)
            
            # Convert total time to a timedelta object
            total_time_delta = datetime.strptime(per_user_average_time, "%H:%M:%S") - datetime(1900, 1, 1)

            # Convert total time to seconds
            total_seconds = total_time_delta.total_seconds()

            # Calculate average time per person
            average_seconds = total_seconds / counter+1

            # Convert average back to timedelta
            average_timedelta = timedelta(seconds=average_seconds)

            # Format average as HH:MM:SS
            user_entry_average_time_str = str(average_timedelta)           
            
            users_average_time.append(user_entry_average_time_str) 


            per_user_entries = [] 
     
        users_entry_average_sum = Entry.sum_list_of_times_into_str(users_average_time)   
        average_time_str = Entry.calculate_average_time(users_entry_average_sum,len(users_average_time))
        return average_time_str


    @staticmethod
    def calculate_total_time():
        return '00:02:00'

    @staticmethod
    def get_effective_time(user_time,average_time):
        
        # Convert string representations to timedelta objects
        user_time = datetime.strptime(user_time, '%H:%M:%S').time()
        average_time = datetime.strptime(average_time, '%H:%M:%S').time()

        # Calculate effective time as timedelta
        effective_time = max(timedelta(hours=user_time.hour, minutes=user_time.minute, seconds=user_time.second) - 
                            timedelta(hours=average_time.hour, minutes=average_time.minute, seconds=average_time.second), 
                            timedelta(0))

        # Convert effective_time back to string if needed
        effective_time_str = str(effective_time)
        return effective_time_str

    @staticmethod
    def get_points_and_expreice_points(total_time,effective_time,constant):
        # Convert string representations to timedelta objects
        total_time = datetime.strptime(total_time, '%H:%M:%S').time()
        effective_time = datetime.strptime(effective_time, '%H:%M:%S').time()

        # Calculate points
        total_time_delta = timedelta(hours=total_time.hour, minutes=total_time.minute, seconds=total_time.second)
        effective_time_delta = timedelta(hours=effective_time.hour, minutes=effective_time.minute, seconds=effective_time.second)

        points = (total_time_delta - effective_time_delta) / total_time_delta * constant
        return points
        

  



            

        