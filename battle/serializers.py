from rest_framework import serializers
from .models import Question, Stock


class QusetionSrializer(serializers.ModelSerializer):
    option = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"

    def get_option(self, obj):
        return list(obj.answer_set.all().values("id", "text"))
    

