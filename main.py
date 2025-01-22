import requests
import uuid
import json
import time
from random import choice 

class CodecademyChat:
    def __init__(self):
        self.headers : dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
            "content-type": "application/json"
        }
        self.cookies : dict = {
            "_cc_exp_id": "".join(choice("wadawdawd") for i in range(6))
        }
        self.recaptcha_token : str = self._solve_captcha()
        self.chat_token : str = None
        self.conversation_id : str = str(uuid.uuid4())

    def _solve_captcha(self) -> str :
        """You need reCaptchaV3 Solver!"""
        return None
        
    def _get_chat_token(self) -> str :
        url = "https://www.codecademy.com/api/portal/anon-chat-token"
        payload = {
            "recaptchaToken": str(self.recaptcha_token),
            "version": 3
        }
        
        response = requests.post(
            url,
            cookies=self.cookies,
            data=json.dumps(payload, separators=(',', ':'))
        )
        self.chat_token = response.text.strip('"')
        return self.chat_token
    
    def send_message(self, message_content) -> json:
        """Send a message to the chat endpoint"""
        if self.chat_token is None:
            self._get_chat_token()
        
        url = "https://www.codecademy.com/api/portal/anon-chat"
        message_id = uuid.uuid4().hex
        timestamp = f"{time.time()}Z"
        payload = {
            "messages": [{
                "id": message_id,
                "role": "user",
                "content": message_content,
                "timestamp": timestamp
            }],
            "chatToken": self.chat_token,
            "conversationId": self.conversation_id
        }
        
        response = requests.post(
            url,
            headers=self.headers,
            cookies=self.cookies,
            json=payload
        )
        return response.json()

if __name__ == "__main__":
    chat = CodecademyChat()
    response = chat.send_message("Hello World!")
    print(response)