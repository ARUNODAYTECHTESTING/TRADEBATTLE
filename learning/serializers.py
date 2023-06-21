from rest_framework import serializers
from .models import UserEnrolment, Question, Answer

class UserEnrolmentSerilizer(serializers.ModelSerializer):

    class Meta:
        exclude = ("user", )
        model = UserEnrolment
        depth = 1

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question


