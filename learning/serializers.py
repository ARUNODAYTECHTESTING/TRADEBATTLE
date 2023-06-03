from rest_framework import serializers
from .models import UserEnrolment

class UserEnrolmentSerilizer(serializers.ModelSerializer):

    class Meta:
        exclude = ("user", )
        model = UserEnrolment
        depth = 1


