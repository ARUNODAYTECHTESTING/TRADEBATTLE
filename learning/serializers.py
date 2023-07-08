from rest_framework import serializers
from .models import UserEnrolment, Question, Lecture, BookMark, Watchlist, Course


class UserEnrolmentSerilizer(serializers.ModelSerializer):

    class Meta:
        exclude = ("user",)
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
        return []


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = "__all__"


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        exclude = ("user",)
        depth = 1


class CourseSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

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
            return (watch_count/all_count)*100
        return 0


