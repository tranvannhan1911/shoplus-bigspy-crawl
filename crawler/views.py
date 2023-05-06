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
import json
from django.http import JsonResponse

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

def api_opera_shoplus_tiktok(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    video_post = VideoPost.from_shoplus(body["data"], VideoPost.BROWSER_OPERA)
    if video_post != None:
        print("[shoplus from opera] "+ str(video_post))
        print()
    return HttpResponse('{"message": "ok"}', content_type='text/plain')

def api_get_ads_id(request):
    ads_id = VideoPost.objects.all().values("ads_id")
    data = []
    for i in ads_id:
        data.append(i["ads_id"])
    print(data)
    return JsonResponse({"data": data})
