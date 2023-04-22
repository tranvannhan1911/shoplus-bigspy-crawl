from .crawlers.bigspy import BigspyCrawler
from .crawlers.shoplus import ShoplusCrawler

def cron_crawl_bigspy():
    crawler = BigspyCrawler("crawl bigspy", 1000)
    crawler.start()


def cron_crawl_shoplus():
    crawler = ShoplusCrawler("crawl shoplus", 1001)
    crawler.start()

