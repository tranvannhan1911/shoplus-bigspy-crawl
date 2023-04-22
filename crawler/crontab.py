from .crawler import crawl_facebook

def my_cron_job():
    print("Crontab")
    crawl_facebook()

