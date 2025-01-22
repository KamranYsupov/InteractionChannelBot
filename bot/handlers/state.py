from aiogram.fsm.state import StatesGroup, State

   
class QuestionState(StatesGroup):
    text = State()
    
     
class FeedBackState(StatesGroup):
    text = State()
    
    
class PostTopicOfferState(StatesGroup):
    text = State()
       
