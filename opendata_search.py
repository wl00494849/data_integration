from dotenv import load_dotenv
from src.chat import Chat
from src.search import search_file

## 向量表檔案太大，如果有需要再聯繫我
## 或用Tool資料夾內的工具自行處理

load_dotenv()
client = Chat()

key = input("請輸入要搜尋的開放資料名稱:")
search_file(keyword=key,top=15)