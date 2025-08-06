from src.integration import Data_Integration
from dotenv import load_dotenv

### 從.env載入環境變數
load_dotenv()

d = Data_Integration(
    filePath1="data/112年國道每月營業額.csv",
    filePath2="data/113年國道每月營業額.csv",
    saveName="result/result.csv",
    model="gpt-4.1-mini"
    )

d.do("幫我加總這兩年的營業額")