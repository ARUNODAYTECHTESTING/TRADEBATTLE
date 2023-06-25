from rest_framework import serializers
from .models import UserEnrolment, Question, Lecture, BookMark

class UserEnrolmentSerilizer(serializers.ModelSerializer):

    class Meta:
        exclude = ("user", )
        model = UserEnrolment
        depth = 1

class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = "__all__"

    def get_answer(self, obj):
        answer = obj.answer_set.all()
        if answer.exists():
            return list(answer.values("text", "id"))
        return[]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = "__all__"

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        exclude = ("user", )
        depth = 1