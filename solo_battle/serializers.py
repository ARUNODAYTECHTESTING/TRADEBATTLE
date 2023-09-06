from rest_framework import serializers
from .models import Battle, QuestionType, Question, Option, QuestionAttempt , Answer , MasterBattle



class MasterBattleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField( read_only = True)
    name = serializers.CharField(max_length=255)
    class Meta:
        model = MasterBattle
        fields = '__all__'
    

class BattleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    battle_status = serializers.CharField(max_length=10)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Battle
        fields = ('id', 'name', 'battle_status', 'created_at', 'updated_at')


class QuestionTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    class Meta:
        model = QuestionType
        fields = ('id', 'name')


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    question_type = serializers.CharField(source='question_type.name')
    battle = serializers.CharField(source='battle.name')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Question
        fields = ('id', 'name', 'question_type', 'battle', 'created_at', 'updated_at')
    
        ref_name = 'QuestionSoloBattle' 


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    question = serializers.IntegerField(source='question.id')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    def create(self, validated_data):
        question = validated_data.pop('question')
        option = Option.objects.create(**validated_data)
        option.question = question
        option.save()
        return option
    class Meta:
        model = Option
        fields = ('id', 'name', 'question', 'created_at', 'updated_at')


class QuestionAttemptSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(source='question.name')
    option = serializers.CharField(source='option.name')
    user = serializers.CharField(source='user.username')
    total_number_of_entry = serializers.IntegerField()
    attempt = serializers.IntegerField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = QuestionAttempt
        fields = ('id', 'question', 'option', 'user', 'total_number_of_entry', 'attempt', 'created_at', 'updated_at')


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    user = serializers.CharField(source='user.username')
    question = serializers.CharField(source='question.name')
    
    class Meta:
        model = Answer
        fields = '__all__'
    
