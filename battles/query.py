from battles import models as battle_models
from datetime import datetime
from shared import utils
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
        return battle_models.SoloBattle.objects.filter(id = id).first()

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
    def validate_max_entries(cls,battle_obj:battle_models.SoloBattle,number_of_entries: int) -> bool:
        if not battle_obj.max_entries >= number_of_entries:
            return False
        return True

    @classmethod
    def check_battle_recurrent_count_with_battle_complete_count(cls):
        pass

    @classmethod
    def create_solo_battle(cls,payload: dict) -> None:  
        battle_models.SoloBattle.objects.create(**payload)

    @classmethod
    def validate_enrollment(cls,battle_obj:battle_models.SoloBattle,enrollment_time: datetime) -> bool:
        if not battle_obj.enrollment_end_time >= enrollment_time:
            return False
        return True
    
    @classmethod
    def validate_entry_fees(cls,battle_obj:battle_models.SoloBattle,entry_fees_paid: int,number_of_entries: int):
        if not battle_obj.entry_fee * int(number_of_entries) == int(entry_fees_paid):
            return False
        return True
    @classmethod
    def prevent_to_enroll_while_battle_live(cls,battle_obj:battle_models.SoloBattle):
        if battle_obj.status in ["live","LIVE","Live"]:
            return True
        return False

class QuestionHandler:
    def __init__(self):
        pass

    @classmethod
    def get_question_object_by_id(cls, id) -> battle_models.QuestionsBase:
       return battle_models.QuestionsBase.objects.filter(id=id).first()
    
