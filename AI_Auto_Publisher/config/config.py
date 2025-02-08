import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """多环境配置管理"""
    
    def __init__(self, env='prod'):
        self.env = env
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        self.accounts = {
            "toutiao": [{
                "username": os.getenv(f"TOUTIAO_USER_{self.env.upper()}"),
                "password": os.getenv(f"TOUTIAO_PWD_{self.env.upper()}")
            }]
        }
        self.proxy = os.getenv(f"PROXY_{self.env.upper()}")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.d_id_api_key = os.getenv("D_ID_API_KEY")

# 使用示例
config = Config('prod')