import os
import json
import logging
import time
from datetime import datetime
from config.config import Config

config = Config()

class AccountManager:
    """智能账号管理系统"""
    
    def __init__(self):
        self.accounts = config.accounts
        self.account_status = self._load_status()
        self.failure_threshold = 3
    
    def _load_status(self):
        """加载账号状态"""
        try:
            with open("account_status.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_status(self):
        """保存账号状态"""
        with open("account_status.json", "w") as f:
            json.dump(self.account_status, f, indent=2)

    def get_available_account(self, platform):
        """选择最优账号"""
        candidates = self.accounts.get(platform, [])
        available = [acc for acc in candidates if self.account_status.get(acc['username'], {}).get('failures', 0) < self.failure_threshold]
        
        if not available:
            raise ValueError("无可用账号")

        selected = min(available, key=lambda x: self.account_status.get(x['username'], {}).get('daily_uses', 0))
        self._update_usage(selected['username'])
        return selected

    def _update_usage(self, username):
        """更新账号使用次数"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.account_status.setdefault(username, {}).setdefault(today, 0)
        self.account_status[username][today] += 1
        self._save_status()