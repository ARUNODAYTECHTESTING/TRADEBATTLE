from rest_framework import serializers
from .models import UserEnrolment, Question, Lecture, BookMark, Watchlist, Course





class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"

    def get_answer(self, obj):
        answer = obj.answer_set.all()
        if answer.exists():
            return list(answer.values("text", "id"))
        return []


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = "__all__"


class BookmarkSerializer(serializers.ModelSerializer):


    class Meta:
        model = BookMark
        exclude = ("user",)
        depth = 3


class CourseSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        depth = 1
        fields = "__all__"

    def get_progress(self, obj):
        user = self.context.get('request').user
        enroll = UserEnrolment.objects.filter(course_id = obj.id, user_id = user.id)
        if enroll.exists():
            enroll = enroll.first()
            watch_count = enroll.watchlist_set.all().count()
            all_count = obj.lecture_set.all().count()
            return int((watch_count/all_count)*100)
        return 0
    
    def get_enrolled(self, obj):
        user = self.context.get('request').user
        return UserEnrolment.objects.filter(course_id = obj.id, user_id = user.id).exists()


class UserEnrolmentSerilizer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        exclude = ("user",)
        model = UserEnrolment
        