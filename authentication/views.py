import random
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_428_PRECONDITION_REQUIRED,
)
from rest_framework.views import APIView

from shared.utils import get_token
from shared.validator import email_validator, password_validator, phone_number_validator

from .models import User
from datetime import datetime
from django.utils.crypto import get_random_string

RANDOM_STRING_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

class UserSendOtpAPI(APIView):
    permission_classes = ()

    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        mobile = request.data.get("mobile", "")
        forget_pass = request.data.get("forget", False)
        user_exist = False
        if mobile and phone_number_validator(mobile):
            user = User.objects.filter(mobile=mobile, mobile_verified=True)
            if user.exists() and forget_pass:
                user = user.first()
                user_exist = True
                user.send_mobile_otp() 
            elif user.exists():
                user_exist = True
            else:

                user, _ = User.objects.get_or_create(
                    mobile = mobile,
                    username = mobile,
                )
                user.referal_code = get_random_string(length=10, allowed_chars=RANDOM_STRING_CHARS)
                user.save()
                user.send_mobile_otp()    
            res_status = HTTP_200_OK
            output_status = True
            message = "Success"   
        else:
            message = "Please provide valid mobile"
        context = {
            "status": output_status,
            "detail": message,
            "user_exist": user_exist
        }
        return Response(context, status=res_status, content_type="application/json")
    
class VerifyOtpView(APIView):

    permission_classes = ()

    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        data = {}
        mobile = request.data.get("mobile", "")
        otp = request.data.get("otp", "")
        if mobile and otp:
            user = User.objects.filter(mobile=mobile)
            if user.exists():
                validity_time = timezone.now() - timedelta(minutes=5)
                user = user.filter(otp_created_at__gte=validity_time)
                if user.exists():
                    user = user.first()
                    if user.otp_code == otp:
                        user.mobile_verified = True
                        user.save()
                        data = get_token(user)
                        res_status = HTTP_200_OK
                        output_status = True
                        message = "Success"
                    else:
                        message = "Invalid otp"
                else:
                    message = "Time limit has been pased"
            else:
                message = "Invalid mobile number"

        else:
            message = "Please provide mobile and otp"

        context = {"status": output_status, "detail": message, "data": data}
        return Response(context, status=res_status, content_type="application/json")
    
class ResendOtpVIew(APIView):

    permission_classes = ()

    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        mobile = request.data.get("mobile", "")
        if mobile and phone_number_validator(mobile):
            user = User.objects.filter(mobile=mobile)
            if user.exists():
                user.first().send_mobile_otp()
                res_status = HTTP_200_OK
                output_status = True
                message = "Success"
            else:
                message = "Mobile is not verified"
        else:
            message = "Mobile is invalid"
        context = {
            "status": output_status,
            "detail": message,
        }
        return Response(context, status=res_status, content_type="application/json")
    
class SetPasswordView(APIView):

    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        password = request.data.get("password")
        if password and password_validator(password):
            user = request.user
            user.set_password(password)
            user.save()
            res_status = HTTP_200_OK
            output_status = True
            message = "Success"
        else:
            message = "Please Provide valid password"

        context = {
                "status": output_status,
                "detail": message,
            }
        return Response(context, status=res_status, content_type="application/json")
    
class LoginView(APIView):

    permission_classes = ()

    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        data = []
        password = request.data.get("password")
        mobile = request.data.get("mobile", "")
        if mobile and password:
            user = User.objects.filter(mobile = mobile)
            if user.exists():
                user = user.first()
                if user.check_password(password):
                    res_status = HTTP_200_OK
                    output_status = True
                    message = "Success"
                    data = get_token(user)
                else:
                    message = "Please provide valid password"
            else:
                message = "Please provide valid mobilee number"
        else:
            message = "Mobile and password are mandatory"

        context = {
                "status": output_status,
                "detail": message,
                "data": data
            }
        return Response(context, status=res_status, content_type="application/json")

class UsernameView(APIView):

    def get(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        username = request.GET.get("username")
        if username:
            obj = User.objects.filter(username = username)
            if not obj.exists():
                res_status = HTTP_200_OK
                output_status = True
                message = "Success"
            else:
                message = "username already exists"
        else:
            message = "username is required"

        context = {
                "status": output_status,
                "detail": message,
            }
        return Response(context, status=res_status, content_type="application/json")



    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        username = request.data.get("username")
        if username:
            if username != request.user.username:
                try: 
                    request.user.username = username
                    request.user.save()
                    res_status = HTTP_200_OK
                    output_status = True
                    message = "Success"
                except Exception as e:
                    message = str(e)
            else:
                message = "Existing username should not be equal to username"
        else:
            message = 'Username is required'
        context = {
                "status": output_status,
                "detail": message,
            }
        return Response(context, status=res_status, content_type="application/json")



