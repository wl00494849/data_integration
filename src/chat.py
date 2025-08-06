import os
from openai import OpenAI,types
from src.mylogger import setup_logger
from datetime import datetime

## OpenAI API串接通用模組
class Chat():

    def __init__(self, api_key:str=None, gpt_model:str=None):
        now = datetime.now()
        self.__api_key = api_key or os.getenv("API_KEY")
        self.gpt_model = gpt_model or "gpt-4o-mini"
        self.client = OpenAI(api_key=self.__api_key)
        self.logger = setup_logger("gpt_api",filePath=f"gpt_api/{now.year}_{now.month}_{now.day}_gpt_api.log")

    def response(self, prompt:str)->types.chat.chat_completion.ChatCompletion:
        messages = []
        messages.append
        {
            "role": "system",
            "content": "請以繁體中文回答。"
        }
        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=messages
        )
        self.__gpt_log(model=self.gpt_model, prompt=prompt, response=response.choices[0].message.content, usage=response.usage)
        return response

    ## size = 0 -> small, size = 1 -> large
    def get_vector(self, term:list,size:int=0)->list:
        model = "text-embedding-3-small"
        if size > 0:
            model = "text-embedding-3-large"
        print(term)
        response = self.client.embeddings.create(
            model=model,
            input=term,
        )
        self.__gpt_log(model=model, prompt=term, usage=response.usage)
        return response.data
    
    def __gpt_log(self,model:str=None, prompt:str|list=None, response:str=None, usage:list=None):
        self.logger.info(f"Use Model: {model}")
        self.logger.info(f"Prompt string: {prompt}")
        self.logger.info(f"Response data: {response}")
        self.logger.info(f"Usage:{usage}")
    

