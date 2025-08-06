from src.extract import extract_by_DF
from src.chat import Chat
from src.mylogger import setup_logger
from pathlib import Path
import pandas as pd
import re

## 資料整合物件
class Data_Integration:
    ### filePath檔案路徑
    ### saveName儲存路徑
    ### model使用GPT模型版本
    def __init__(self,filePath1:str,filePath2:str,saveName:str="data/result",model:str=""):
        self.df1 = pd.read_csv(filePath1)
        self.df2 = pd.read_csv(filePath2)
        self.fileName1 = Path(filePath1).name
        self.fileName2 = Path(filePath2).name
        self.field1 = extract_by_DF(self.df1)
        self.field2 = extract_by_DF(self.df2)
        self.client = Chat(gpt_model=model)
        self.saveName = saveName
        self.total_tokens = 0
        self.total_error=0
        self.fail = False

    ## 採用CoT
    def do(self,prompt:str):
        result = self.__flow(prompt)
        if not result.empty:
            result.to_csv(f"{self.saveName}.csv",index=False)
    
    ## 未採用CoT
    def do_no_CoT(self,prompt:str):
        result = self.__no_CoT_flow(prompt)
        if not result.empty:
            result.to_csv(f"{self.saveName}.csv",index=False)
    
    ## 採用CoT流程
    def __flow(self,prompt:str)->pd.DataFrame:
        stmp = self.__get_stmp(prompt)
        code = self.__get_code(prompt=prompt,stmp=stmp)
        result = self.__exce_merge(code,stmp,prompt)
        print(self.total_tokens)
        self.__write_log(f"total_tolen={self.total_tokens}")
        return result

    ## 未採用CoT流程
    def __no_CoT_flow(self,prompt:str)->pd.DataFrame:
        code = self.__get_code(prompt=prompt,stmp="")
        result = self.__exce_merge(code,"",prompt)
        print(self.total_tokens)
        self.__write_log(f"total_tolen={self.total_tokens}")
        return result

    ## GPT生成程式碼
    def __get_code(self,prompt:str,stmp:str)->str:
        rep = self.client.response(self.__generate_pandas_code(prompt,stmp))
        content = rep.choices[0].message.content
        self.total_tokens += rep.usage.total_tokens
        print(content)
        self.__write_log(content)
        return content

    ## GPT制定流程
    def __get_stmp(self,prompt:str)->str:
        rep = self.client.response(self.__cot_prompt(prompt))
        content = rep.choices[0].message.content
        self.total_tokens += rep.usage.total_tokens
        print(content)
        self.__write_log(content)
        return content

    ## GPT執行程式碼
    def __exce_merge(self,code:str,stmp:str,prompt:str,count:int=0):
        try:
            import pandas as pd
            code = code.strip('`')
            code = re.sub(r"^python", "", code, flags=re.MULTILINE)

            df1 = self.df1
            df2 = self.df2
            
            exec(code,locals(),globals())
            
            return result
            
        except Exception as err:
            if count > 3:
                print("Error")
                self.fail = True
                return pd.DataFrame

            self.total_error += 1
            print(f"第{count}次修復")
            print(f"錯誤訊息：{err}")
            rep = self.client.response(self.__pandas_error_handling(stmp,prompt,code,err))
            code = rep.choices[0].message.content
            self.total_tokens += rep.usage.total_tokens
            print(code)
            self.__write_log(f"第{count}次修復\n錯誤訊息：{err}\n{code}")
            return self.__exce_merge(code,stmp,prompt,count+1)

    def __write_log(self,message):
        with open(f"{self.saveName}_gpt_api.txt", 'a', encoding='utf-8') as f:
            f.write(message + '\n')
            f.write("==================================" + "\n")

    ### 制定檔案合併流程
    ### prompt = 使用者的要求
    def __cot_prompt(self,prompt:str)->str:
        return f"""
        有兩個已經存在的 pandas DataFrame 其變數為df1,df2
        無需再重複定義df1,df2
        ###
        df1 fileName = {self.fileName1}
        df2 fileName = {self.fileName2}
        ###
        col最左邊 = 最前面 = index為0
        df1 col:{self.field1[0]}
        df2 col:{self.field2[0]}
 
        ###
        df1 前10筆資料為:{self.field1[1]}
        df2 前10筆資料為:{self.field2[1]}
        ###

        要求：
        {prompt}

        先統整需求跟解讀資料結構、型別，再思考如何解決問題
        限制：
        僅制訂處理步驟即可，不需要提供程式碼
        Let's think step by step
        """

    ### 生成pandas程式碼提示樣板
    ### flow = GPT Project Manager 制定的流程
    ### prompt = 使用者的要求
    def __generate_pandas_code(self,prompt:str,flow:str)->str:
        return f"""
        有兩個已經存在的 pandas DataFrame df1,df2
        無需再重複定義df1,df2
        ###
        df1 fileName = {self.fileName1}
        df2 fileName = {self.fileName2}
        ###
        col最左邊 = 最前面 = index為0
        df1 col:{self.field1[0]}
        df2 col:{self.field2[0]}
        ###
        df1 前10筆資料為:{self.field1[1]}
        df2 前10筆資料為:{self.field2[1]}

        步驟：
        {flow}
        要求：
        {prompt}

        根據步驟逐步生成pandas程式碼
        pandas版本為2.2.3
        
        並根據以下規則做最後的回答：
        1.合併結果變數為result的DataFrame
        2.只要給我python exce()可以執行的pandas程式碼
        3.不要註解，不要額外解釋
        4.不需要import pandas
        """

    ### pandas程式碼錯誤處理
    def __pandas_error_handling(self,flow:str,prompt:str,code:str,err:str)->str:
        return f"""
        步驟：
        {flow}
        要求：
        {prompt}

        根據資訊給予pandas程式碼
        pandas版本為2.2.3

        並根據以下規則做最後的回答：
        1.合併結果變數為result
        2.只要給我python exce()可以執行的pandas程式碼
        3.不要註解，不要額外解釋
        4.不需要import pandas

        生成程式碼：
        {code}
        錯誤訊息：
        {err}
        請重新生成程式碼
        """