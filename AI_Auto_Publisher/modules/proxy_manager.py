import requests
import json
import random

class ProxyManager:
    """代理管理系统"""

    def __init__(self, proxy_file="proxies.json"):
        self.proxy_file = proxy_file
        self.proxies = self._load_proxies()
    
    def _load_proxies(self):
        """加载代理"""
        try:
            with open(self.proxy_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_proxies(self):
        """保存代理"""
        with open(self.proxy_file, "w") as f:
            json.dump(self.proxies, f, indent=2)
    
    def get_proxy(self):
        """获取随机代理"""
        return random.choice(self.proxies) if self.proxies else None

    def refresh_proxies(self):
        """从代理池更新代理"""
        sources = ["https://proxy-source.com/api/get"]
        new_proxies = []
        
        for url in sources:
            try:
                response = requests.get(url, timeout=10)
                new_proxies.extend(response.json().get("proxies", []))
            except:
                pass
        
        self.proxies = new_proxies
        self._save_proxies()