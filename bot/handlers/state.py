from aiogram.fsm.state import StatesGroup, State

   
class RuQuestionState(StatesGroup):
    text = State()
    
     
class RuFeedBackState(StatesGroup):
    text = State()
    
    
class RuPostTopicOfferState(StatesGroup):
    text = State()
    

class EnQuestionState(StatesGroup):
    text = State()
    
     
class EnFeedBackState(StatesGroup):
    text = State()
    
    
class EnPostTopicOfferState(StatesGroup):
    text = State()
       

class FormatedTextState(StatesGroup):
    text = State()       
       

