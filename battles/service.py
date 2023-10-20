from battles import query as battle_query
from django.http import HttpRequest
from battles import serializers as battle_serializers
from shared import utils
class SoloBattleService:
    def __init__(self):
        pass
    
    @staticmethod
    def validate_solo_battle_request(payload: dict):
        try:
            market_type_obj = battle_query.MarketTypeHandler.get_market_type_object_by_id(payload['market_type'])
            battle_category_obj = battle_query.BattleCategoryHandler.get_battle_category_object_by_id(payload['category'])

            if len(payload['questions_set']) > 0:
                question_obj = battle_query.QuestionHandler.get_question_object_by_id(payload['questions_set'][0])
                if question_obj is None:
                    return 400,f"Question not found associated with id's {payload['questions_set'][0]}"
                
            if market_type_obj is None:
                return 400, f"Market type not found associated with id's {payload['market_type']}"
            
            if battle_category_obj is None:
                return 400, f"Battle category not found associated with id's {payload['category']}"
            
            payload['market_type'] = market_type_obj
            payload['category'] = battle_category_obj
            battle_query.SoloBattleHandler.create_solo_battle(payload)  
            return 200, "Battle created successfully"    
        except Exception as e:
            return 400, e
        

    
class QuestionService:
    def __init__(self):
        pass

    def calculates_question_votes_percent():
        pass


class SoloBattleUserService:

    @staticmethod
    def validate_solo_battle_User_request(request: HttpRequest):
        try:
            # TODO: Validate request body
            serializer = battle_serializers.SoloBattleUserQuestionAnswerSerializer(data = request.data)
            if not serializer.is_valid():
                return 400, serializer.errors
            battle_obj = battle_query.SoloBattleHandler.get_solo_battle_object_by_id(serializer.data['battle'])
            if battle_obj is None:
                return 400, f"Battle not found associated with id '{serializer.data['battle']}'"
            
            elif not battle_query.SoloBattleHandler.validate_max_entries(battle_obj,serializer.data['number_of_entries']):
                return 400, f"Entry can't be allowed more than {battle_obj.max_entries}"
            elif not battle_query.SoloBattleHandler.validate_enrollment(battle_obj,utils.DateTimeConversion.str_datetime_into_datetime_obj(serializer.data['enrollment_time'])):
                return 400, f"Entrollment time expired. at {battle_obj.enrollment_end_time}"
            
            elif not battle_query.SoloBattleHandler.validate_entry_fees(battle_obj,serializer.data['entry_fees_paid'],serializer.data['number_of_entries']):
                return 400, f"Insufficient entry fees paid"
            
            serializer.save(battle = battle_obj,user = request.user)
            return 200, f"Question answer created successfully"
        
        except Exception as e:
            return 400, e