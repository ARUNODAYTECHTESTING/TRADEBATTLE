from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from decouple import config

class ForkedAuthentication(JWTAuthentication):


    def authenticate(self, request):
        return_tuple = super(ForkedAuthentication,self).authenticate(request)
        if return_tuple:
            user , validated_token = return_tuple 

            key = user.id
            if not cache.get(key):
                cache.set(key,True,timeout = 86400)
                user.experience_point += config("DAILY_POINT", 10, cast = int)
                user.save()
            return user, validated_token

