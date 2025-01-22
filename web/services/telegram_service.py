import requests


class TelegramService:
    def __init__(
        self,
        bot_token: str,
        api_url: str ,
    ):
        self.__bot_token = bot_token
        self.api_url = api_url
       
    @property
    def __bot_api_url(self):
        return f'{self.api_url}/bot{self.__bot_token}'
        
    def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: dict[str, list] | None = None,
        parse_mode: str = 'HTML',
    ):
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
        }
    
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
    
        response = requests.post(
            url=f'{self.__bot_api_url}/sendMessage', 
            json=payload,
        )
    
        return response
    
    def send_poll(
        self,
        chat_id: int,
        question: str,
        options: list[str],
        is_anonymous: bool = False,
    ):
        payload = {
            'chat_id': chat_id,
            'question': question,
            'options': options,
            'is_anonymous': is_anonymous,
        }
    
        response = requests.post(
            url=f'{self.__bot_api_url}/sendPoll', 
            json=payload,
        )
    
        return response
    
    
    def forward_message(
        self,
        chat_id: int,
        from_chat_id: int,
        message_id: int,
    ):
        payload = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
        }

    
        response = requests.post(
            url=f'{self.__bot_api_url}/forwardMessage', 
            json=payload,
        )
    
        return response