from battles import models as battle_models

class MarketTypeHandler:

    @classmethod
    def get_market_type_object_by_id(cls,id) -> battle_models.MarketType:
        return battle_models.MarketType.objects.filter(id = id).first() 

class BattleCategoryHandler:
    @classmethod
    def get_battle_category_object_by_id(cls,id) -> battle_models.BattleCategory:
        return battle_models.BattleCategory.objects.filter(id = id).first() 

class SoloBattleHandler:

    @classmethod
    def get_solo_battle_object_by_id(cls,id: int) -> battle_models.SoloBattle:
        pass

    @classmethod
    def validate_battle_start_end_time(cls,start_time,end_time):
        # TODO: check once battle create
        pass

    @classmethod
    def validate_enrollment_start_end_time(cls,start_time,end_time):
        # TODO: check once battle
        pass

    @classmethod
    def update_battle_status(cls):
        # TODO: check every seconds once battle created using cronjob
        pass

    @classmethod
    def validate_max_participants(cls):
        # TODO: check once enduser wants to enrolled in battle
        pass

    @classmethod
    def validate_max_entries(cls):
        pass

    @classmethod
    def check_battle_recurrent_count_with_battle_complete_count(cls):
        pass

    @classmethod
    def create_solo_battle(cls,payload: dict) -> None:  
        battle_models.SoloBattle.objects.create(**payload)

class QuestionHandler:
    def __init__(self):
        pass

    @classmethod
    def get_question_object_by_id(cls, id) -> battle_models.QuestionsBase:
       return battle_models.QuestionsBase.objects.filter(id=id).first()
    
