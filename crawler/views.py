from django.shortcuts import render
from .crawlers.bigspy import BigspyCrawler
from .crawlers.shoplus import ShoplusCrawler
from django.shortcuts import redirect
from django.urls import reverse
import threading
import os
import socialcrawler.settings as settings
from django.http import HttpResponse

def dashboard_view(request):
    for thread in threading.enumerate(): 
        print(thread.name)
    return "home"

def bigspy_crawl_view(request):
    crawler = BigspyCrawler("crawl bigspy", 1000)
    crawler.start()
    return redirect("/admin/crawler/videopost/")

def shoplus_crawl_view(request):
    crawler = ShoplusCrawler("crawl shoplus", 1001)
    crawler.start()
    return redirect("/admin/crawler/videopost/")

def log_view(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'log.log')
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_content = log_file.read()
    return HttpResponse(log_content, content_type='text/plain')
