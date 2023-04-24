from .crawlers.bigspy import BigspyCrawler
from .crawlers.shoplus import ShoplusCrawler
from .models import VideoPost

def cron_crawl_bigspy_facebook():
    crawler = BigspyCrawler("crawl bigspy facebook", 1000, VideoPost.PLATFORM_FACEBOOK)
    crawler.start()

def cron_crawl_bigspy_tiktok():
    crawler = BigspyCrawler("crawl bigspy tiktok", 1001, VideoPost.PLATFORM_TIKTOK)
    crawler.start()

def cron_crawl_shoplus():
    crawler = ShoplusCrawler("crawl shoplus", 2000)
    crawler.start()

def test():
    print("hello cron job!")

