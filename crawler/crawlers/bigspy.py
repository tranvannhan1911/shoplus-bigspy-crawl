import time

# from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from crawler.models import VideoPost, AccountCrawlerConfig, SeleniumCrawlerConfig
import json
import crawler.api as api
import threading
import traceback
import platform
import logging
logger = logging.getLogger("django")

class BigspyCrawler(threading.Thread):
    def __init__(self, thread_name, thread_ID, platform_crawl):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.platform_crawl = platform_crawl

    def run(self):
        self.crawl()

    def crawl(self):
        account_crawler_config = AccountCrawlerConfig.objects.first()
        selenium_crawler_config = SeleniumCrawlerConfig.objects.first()
        max_tries_all = 10
        crawled_count = 0
        while max_tries_all > 0:
            selenium_crawler_config.bigspy_running = True
            selenium_crawler_config.save()
            try:
                logger.info("Start crawl bigspy "+str(self.platform_crawl)+"...")
                chrome_options = Options()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument("--headless")
                capabilities = webdriver.DesiredCapabilities.CHROME
                capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
                executable_path = r'./chromedriver'
                if platform.system() == 'Windows':
                    executable_path = r'./chromedriver.exe'
                driver = webdriver.Chrome(executable_path=executable_path, desired_capabilities=capabilities, options=chrome_options)
                driver.set_window_size(1500, 1000)

                driver.get('https://www.henull.com/auth/login')
                time.sleep(5)
                input_email = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type=email]")))
                input_password = driver.find_element(By.CSS_SELECTOR, 'input[type=password]')
                btn_login = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
                input_email.send_keys(account_crawler_config.henull_username)
                input_password.send_keys(account_crawler_config.henull_password)
                btn_login.click()

                WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/tools']")))
                driver.get('https://www.henull.com/tools')

                bigspy_text = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'BigSpy VIP Enterprise')]")))
                # bigspy_text = driver.find_element_by_xpath("//span[contains(text(), 'BigSpy VIP Enterprise')]")
                bigspy_card = bigspy_text.find_element(By.XPATH, "../..")
                bigspy_btn = bigspy_card.find_element(By.CSS_SELECTOR, "button[type=button]")
                bigspy_btn.click()
                time.sleep(10)
                driver.switch_to.window(driver.window_handles[0])
                max_tries = 1
                while(max_tries > 0):
                    try:
                        driver.get('https://l9gr5r2r.realnull.com/adspy/facebook/?utm_home=1')
                        # try:
                        #     btn_close_ads = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#popup-content > div.close-button")))
                        #     btn_close_ads.click()
                        # except:
                        #     print("Không có quảng cáo")
                        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#popup-content > div.close-button")))
                        break
                    except:
                        max_tries -= 1
                        pass
                
                time.sleep(10)

                def process_browser_logs_for_network_events(logs):
                    """
                    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
                    since we're interested in the network events specifically.
                    """
                    for entry in logs:
                        log = json.loads(entry["message"])["message"]
                        if (
                                "Network.response" in log["method"]
                                or "Network.request" in log["method"]
                                or "Network.webSocket" in log["method"]
                        ):
                            yield log
                logs = driver.get_log("performance")

                events = process_browser_logs_for_network_events(logs)
                token = None
                cookie = None
                for event in events:
                    if "headers" in event["params"].keys() and "authorization" in event["params"]["headers"].keys() and event["params"]["headers"]["authorization"].startswith("ey"):
                        token = event["params"]["headers"]["authorization"]
                        cookie = event["params"]["headers"]["cookie"]
                        # print(event)
                        # print()

                if token == None or cookie == None:
                    raise Exception("Token or cookie is None")

                self.token = token
                self.cookie = cookie
                logger.info("token: "+ token)
                logger.info("cookie: "+ cookie)
                driver.quit()
                max_page = 100
                for page in range(1, max_page+1):
                    tries_list = 2
                    data = None
                    while(tries_list > 0):
                        try:
                            data = self.crawl_list(page)
                            break
                        except:
                            tries_list -= 1
                            time.sleep(1)
                    if data != None:
                        for post in data["data"]:
                            try:
                                if VideoPost.objects.filter(ads_id=post["ad_key"]).exists():
                                    continue
                                detail = api.get_bigspy_henull_ads_detail(post["ad_key"], token, cookie)
                                # print(detail)
                                video_post = VideoPost.from_bigspy(detail["data"], self.platform_crawl)
                                if video_post != None:
                                    crawled_count += 1
                                    logger.info("[bigspy "+ str(self.platform_crawl) + ": " + str(crawled_count) +"] "+ str(video_post))
                                    logger.info("\n")
                                    # if(crawled_count % 5 == 0):
                                    selenium_crawler_config.bigspy_crawled = crawled_count
                                    selenium_crawler_config.save()
                            except Exception:
                                logger.error(traceback.format_exc())
                                # logger.info(post)
            except Exception:
                logger.error(traceback.format_exc())
                selenium_crawler_config.bigspy_running = False
                selenium_crawler_config.save()
                max_tries_all -= 1

    def crawl_list(self, page):
        if self.platform_crawl == VideoPost.PLATFORM_FACEBOOK:
            return api.get_bigspy_henull_facebook_ads_list(page, self.token, self.cookie)
        
        if self.platform_crawl == VideoPost.PLATFORM_TIKTOK:
            return api.get_bigspy_henull_tiktok_ads_list(page, self.token, self.cookie)

 