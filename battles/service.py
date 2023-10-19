from battles import query as battle_query

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