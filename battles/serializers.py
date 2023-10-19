from rest_framework import serializers
from .models import (
    MarketType,
    BattleCategory,
    TimeBattle,
    TimeBattleUser,
    SoloBattle,
    SoloBattleUser,
    LeagueBattle,
    LeagueBattleUser,
    PredictBattle,
    PredictBattleUser,
    QuestionsBase
  
)

class MarketTypeSerializer(serializers.ModelSerializer):
    """Serializer for the MarketType model."""

    class Meta:
        model = MarketType
        fields = ('id', 'name', 'max_entries')


class BattleCategorySerializer(serializers.ModelSerializer):
    """Serializer for the BattleCategory model."""

    class Meta:
        model = BattleCategory
        fields = ('id', 'name')


class TimeBattleSerializer(serializers.ModelSerializer):
    """Serializer for the TimeBattle model."""

    class Meta:
        model = TimeBattle
        fields = (
            'id',
            'name',
            'market_type',
            'category',
            'battle_image',
            'enrollment_start_time',
            'enrollment_end_time',
            'battle_start_time',
            'battle_end_time',
            'status',
            'battle_recurrent_count',
            'battle_frequency',
            'trivia',
            'coins_multiplier_constant',
            'experience_points_multiplier_constant',
            'max_winnings',
            'max_participants',
            'entry_fee',
            'questions_set',
        )


class TimeBattleUserSerializer(serializers.ModelSerializer):
    """Serializer for the TimeBattleUser model."""

    class Meta:
        model = TimeBattleUser
        fields = (
            'id',
            'user',
            'battle_id',
            'submitted_time_and_answers',
            'total_answer_duration',
            'enrollment_time',
            'status',
            'coins_earned',
            'experience_points_earned',
            'entry_fees_paid',
            'questions_set',
        )


class SoloBattleSerializer(serializers.ModelSerializer):
    """Serializer for the SoloBattle model."""

    class Meta:
        model = SoloBattle
        fields = "__all__"


class SoloBattleUserSerializer(serializers.ModelSerializer):
    """Serializer for the SoloBattleUser model."""

    class Meta:
        model = SoloBattleUser
        fields = (
            'id',
            'user',
            'battle',
            'number_of_entries',
            'submitted_time_and_answers',
            'enrollment_time',
            'status',
            'coins_earned',
            'experience_points_earned',
            'entry_fees_paid',
        )




class PredictBattleSerializer(serializers.ModelSerializer):
    """Serializer for the PredictBattle model."""

    class Meta:
        model = PredictBattle
        fields = (
            'id',
            'name',
            'market_type',
            'category',
            'battle_image',
            'enrollment_start_time',
            'enrollment_end_time',
            'battle_start_time',
            'battle_end_time',
            'status',
            'battle_recurrent_count',
            'battle_frequency',
            'trivia',
            'coins_multiplier_constant',
            'experience_points_multiplier_constant',
            'max_winnings',
            'max_participants',
            'entry_fee',
            'max_allowed_stocks',  
            'multiplier_options', 
            'max_entries', 
            'questions_set', 
        )

class PredictBattleUserSerializer(serializers.ModelSerializer):
    """Serializer for the PredictBattleUser model."""

    class Meta:
        model = PredictBattleUser
        fields = (
            'id',
            'user',
            'battle',
            'number_of_entries',
            'submitted_time_and_answers',
            'enrollment_time',
            'total_answer_duration',
            'coins_earned',
            'status',
            'experience_points_earned',
            'entry_fees_paid',
        )
        
        
        

#League Battle
class LeagueBattleSerializer(serializers.ModelSerializer):
    """Serializer for the LeagueBattle model."""

    class Meta:
        model = LeagueBattle
        fields = (
            'id',
            'name',
            'market_type',
            'category',
            'battle_image',
            'enrollment_start_time',
            'enrollment_end_time',
            'battle_start_time',
            'battle_end_time',
            'status',
            'battle_recurrent_count',
            'battle_frequency',
            'trivia',
            'coins_multiplier_constant',
            'experience_points_multiplier_constant',
            'max_winnings',
            'max_participants',
            'entry_fee',
            'max_allowed_stocks',  
            'multiplier_options', 
            'max_entries', 
        )


class LeagueBattleUserSerializer(serializers.ModelSerializer):
    """Serializer for the LeagueBattleUser model."""

    class Meta:
        model = LeagueBattleUser
        fields = (
            'id',
            'user',
            'battle',
            'number_of_entries',
            'submitted_time_and_answers',
            'enrollment_time',
            'total_answer_duration',
            'coins_earned',
            'status',
            'experience_points_earned',
            'entry_fees_paid',
        )

# TODO: QuestionBase serializer
class QuestionBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionsBase
        fields = "__all__"