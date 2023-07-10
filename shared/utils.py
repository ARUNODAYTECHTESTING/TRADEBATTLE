from rest_framework_simplejwt.tokens import RefreshToken
import requests
import logging
from typing import Tuple

def get_token(user_object):
    refresh = RefreshToken.for_user(user_object)
    token = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return token

class RequestToClient:
  
    @staticmethod
    def _get(end_point : str,headers: dict = None) -> Tuple[int,dict]:
        try:
            response = requests.get(end_point,headers=headers)
            if response.status_code == 200:
                return 200, response.json()
            
            return 400,response.json()
        except Exception as e:
            return 400,str(e)

