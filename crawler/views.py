from django.shortcuts import render
from .crawlers.bigspy import BigspyCrawler
from .crawlers.shoplus import ShoplusCrawler
from django.shortcuts import redirect
from django.urls import reverse
import threading
import os
import socialcrawler.settings as settings
from django.http import HttpResponse
from crawler.models import VideoPost

def dashboard_view(request):
    for thread in threading.enumerate(): 
        print(thread.name)
    return "home"

def bigspy_facebook_crawl_view(request):
    crawler = BigspyCrawler("crawl bigspy facebook", 1000, VideoPost.PLATFORM_FACEBOOK)
    crawler.start()
    return redirect("/admin/crawler/videopost/")

def bigspy_tiktok_crawl_view(request):
    crawler = BigspyCrawler("crawl bigspy tiktok", 1001, VideoPost.PLATFORM_TIKTOK)
    crawler.start()
    return redirect("/admin/crawler/videopost/")

def shoplus_crawl_view(request):
    crawler = ShoplusCrawler("crawl shoplus", 2000)
    crawler.start()
    return redirect("/admin/crawler/videopost/")

def log_view(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'log.log')
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_content = log_file.read()
    return HttpResponse(log_content, content_type='text/plain')
