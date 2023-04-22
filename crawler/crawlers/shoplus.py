import time

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import json
import pprint
import crawler.api as api
import threading
from crawler.models import VideoPost, AccountCrawlerConfig, SeleniumCrawlerConfig
from datetime import datetime
import traceback
import logging
logger = logging.getLogger("django")


class ShoplusCrawler(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

    def run(self):
        self.crawl()

    def crawl(self):
        account_crawler_config = AccountCrawlerConfig.objects.first()
        selenium_crawler_config = SeleniumCrawlerConfig.objects.first()
        max_tries_all = 50
        crawled_count = 0
        while max_tries_all > 0:
            selenium_crawler_config.shoplus_running = True
            selenium_crawler_config.save()
            try:
                logger.info("Start crawl shoplus...")
                chrome_options = Options()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument("--headless")
                capabilities = webdriver.DesiredCapabilities.CHROME
                capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
                # , desired_capabilities=capabilities, options=options
                # driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
                driver = webdriver.Chrome(executable_path=r'./chromedriver', desired_capabilities=capabilities, options=chrome_options)
                driver.set_window_size(1500, 1000)

                driver.get('https://www.shoplus.net/login')
                time.sleep(5)

                input_email = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/form/div[2]/div/div[1]/input')))
                input_password = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type=password]")))

                input_email.send_keys(account_crawler_config.shoplus_username)
                input_password.send_keys(account_crawler_config.shoplus_password)
                btn_login = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/div/div[2]/form/div[6]/div/button")))
                btn_login.click()
                time.sleep(7)
                driver.get("https://www.shoplus.net/discovery/ads")
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
                    if "headers" in event["params"].keys() and "authorization" in event["params"]["headers"].keys() and event["params"]["headers"]["authorization"].startswith("Bearer") and "cookie" in event["params"]["headers"].keys():
                        token = event["params"]["headers"]["authorization"]
                        cookie = event["params"]["headers"]["cookie"]

                logger.info("token: "+ token)
                logger.info("cookie: "+ cookie)
                driver.quit()
                max_page = 49
                for page in range(0, max_page+1):
                    data = api.get_shoplus_ads_list(page, token, cookie)
                    # print(data)
                    # print()
                    for post in data["data"]["items"]:
                        # try:
                        if VideoPost.objects.filter(ads_id=post["id"]).exists():
                            continue
                        last_time_seconds = post["last_time"] // 1000
                        last_time_date = datetime.fromtimestamp(last_time_seconds).strftime('%Y-%m-%d')
                        detail = api.get_shoplus_ads_detail(post["id"], post["author_id"], post["video_id"], last_time_date, token, cookie)
                        video_post = VideoPost.from_shoplus(detail["data"])
                        if video_post != None:
                            crawled_count += 1
                            logger.info("[shoplus "+ str(crawled_count) +"] "+ str(video_post))
                            logger.info("\n")
                            selenium_crawler_config.shoplus_crawled = crawled_count
                            selenium_crawler_config.save()
                        time.sleep(1)
                        # except Exception as e:
                        #     print("Failure", e)
                        #     print(post)
                break
            except Exception:
                logger.error(traceback.format_exc())
                selenium_crawler_config.shoplus_running = False
                selenium_crawler_config.save()
                max_tries_all -= 1