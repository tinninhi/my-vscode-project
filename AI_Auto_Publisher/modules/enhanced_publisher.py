import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from modules.account_manager import AccountManager
from modules.proxy_manager import ProxyManager

class EnhancedPublisher:
    """自动发布系统"""

    def __init__(self, platform):
        self.platform = platform
        self.account_manager = AccountManager()
        self.proxy_manager = ProxyManager()
        self.driver = self._setup_driver()
    
    def _setup_driver(self):
        """初始化浏览器"""
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        proxy = self.proxy_manager.get_proxy()
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def login_and_publish(self, article):
        """登录并发布"""
        account = self.account_manager.get_available_account(self.platform)
        self.driver.get("https://mp.toutiao.com/login/")
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "account"))
        ).send_keys(account["username"])
        
        self.driver.find_element(By.NAME, "password").send_keys(account["password"])
        self.driver.find_element(By.XPATH, "//button[text()='登录']").click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='请输入标题']"))
        ).send_keys(article["title"])

        self.driver.find_element(By.XPATH, "//div[@class='editor-container']").send_keys(article["content"])
        self.driver.find_element(By.XPATH, "//button[text()='发布']").click()