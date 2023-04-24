from django.db import models
from django_countries.fields import CountryField
from .utils import to_number, country_to_str, clean_str
from datetime import datetime
import json
from preferences.models import Preferences
from gsheets import mixins
from uuid import uuid4
from django.utils import timezone
from .storage import OverwriteStorage

# class Country(models.Model):
#     country = CountryField()

class VideoPost(mixins.SheetPushableMixin, models.Model):
    PLATFORM_FACEBOOK = "facebook"
    PLATFORM_TIKTOK = "tiktok"
    CRAWLER_BIGSPY = "bigspy"
    CRAWLER_SHOPLUS = "shoplus"

    spreadsheet_id = '1U2wy1EpGqcwAR9HJTunk0jNLfzYm-yQY48cS8DI_wHY'
    model_id_field = 'ads_id'
    sheet_name = 'Sheet1'
    sheet_id_field = 'ads_id'

    ads_id = models.CharField('Ads id', max_length=255)
    title = models.CharField("Tiêu đề", max_length=255, default="", blank=True)
    fanpage_name = models.CharField('Tên fanpage', max_length=255, default="", blank=True)
    fanpage_url = models.CharField('Link fanpage', max_length=255, default="", blank=True)
    # country = CountryField('Quốc gia')
    country = models.CharField("Quốc gia", max_length=255, default="Việt Nam")
    content = models.TextField('Nội dung', default="", blank=True)
    thumbnail_url = models.CharField('Thumbnail', max_length=255, default="", blank=True)
    avatar = models.CharField('Avatar', max_length=255, default="", blank=True)
    video_url = models.CharField('Video URL', max_length=255, default="", blank=True)
    platform = models.CharField('Nền tảng', max_length=255, choices=(
        (PLATFORM_FACEBOOK, PLATFORM_FACEBOOK), (PLATFORM_TIKTOK, PLATFORM_TIKTOK)
    ))
    landing_page_url = models.CharField('Landing Page URL', max_length=255, default="", blank=True)
    resolution = models.CharField('Độ phân giải', max_length=255, default="", blank=True)
    original_post_url = models.CharField('Bài viết gốc', max_length=255, default="", blank=True)
    impression_count = models.IntegerField('Impression', default=0)
    like_count = models.IntegerField('Lượt like', default=0)
    comment_count = models.IntegerField('Lượt bình luận', default=0)
    share_count = models.IntegerField('Lượt share', default=0)
    created_at = models.DateTimeField('Ngày thu thập', auto_now_add=True)
    posted_at = models.DateTimeField('Ngày đăng')
    crawler = models.CharField("Nền tảng cào", max_length=255, choices=(
        (CRAWLER_BIGSPY, CRAWLER_BIGSPY), (CRAWLER_SHOPLUS, CRAWLER_SHOPLUS)
    ))

    @classmethod
    def get_sheet_push_fields(cls):
        lst = [f.name for f in cls._meta.fields]
        lst.append("posted_at_time")
        lst.append("created_at_time")
        return lst

    @property
    def posted_at_time(self):
        local_time = timezone.localtime(self.posted_at, timezone=timezone.get_fixed_timezone(420))
        return local_time.strftime("%H:%M, %d/%m/%Y")

    @property
    def created_at_time(self):
        local_time = timezone.localtime(self.created_at, timezone=timezone.get_fixed_timezone(420))
        return local_time.strftime("%H:%M, %d/%m/%Y")

    def __str__(self):
        return self.title
    
    @staticmethod
    def from_bigspy(data, platform):
        if VideoPost.objects.filter(ads_id=data["ad_key"]).exists():
            print("ads id: " + data["ad_key"] + " đã tồn tại")
            return None
        
        save_data = {
            "ads_id": data["ad_key"],
            "title": clean_str(data["title"]),
            "fanpage_name": clean_str(data["page_name"]),
            # "country": "VN",
            "thumbnail_url": data["preview_img_url"].replace("https://l9gr64nv.realnull.com", "https://sp2cdn-idea-global.zingfront.com"),
            "fanpage_url": data["store_url"],
            "avatar": data["logo_url"],
            "video_url": json.loads(data["cdn_url"])[0].replace("https://l9gr64nv.realnull.com", "https://sp2cdn-idea-global.zingfront.com"),
            "platform": platform,
            "content": clean_str(data["message"]),
            "posted_at": datetime.fromtimestamp(data["created_at"]),
            "landing_page_url": data["store_url"],
            "resolution": str(data["ad_width"]) + "*" + str(data["ad_height"]),
            "original_post_url": data["source_url"],
            "impression_count": to_number(data["impression"]),
            "like_count": to_number(data["like_count"]),
            "comment_count": to_number(data["comment_count"]),
            "share_count": to_number(data["share_count"]),
            "crawler": VideoPost.CRAWLER_BIGSPY
        }
        video_post = VideoPost.objects.create(**save_data)
        return video_post
    
    def save(self, *args, **kwargs):
        super(VideoPost, self).save(*args, **kwargs)
        self.push_to_sheet()
    
    @staticmethod
    def from_shoplus(data):
        if VideoPost.objects.filter(ads_id=data["id"]).exists():
            print("ads id: " + str(data["id"]) + " đã tồn tại")
            return None
        
        save_data = {
            "ads_id": data["id"],
            "title": clean_str(data["desc"]),
            "fanpage_name": clean_str(data["nickname"]),
            # "country": "VN",
            "thumbnail_url": "https://t-img.picturehaven.net/tikmeta/"+ data["origin_cover_privatization"] +"?imageMogr2/auto-orient/thumbnail/360x/strip/format/WEBP/quality/75!/ignore-error/1",
            "fanpage_url": "",
            "avatar": "https://t-img.picturehaven.net/tikmeta/"+data["avatar_privatization"]+"?imageMogr2/auto-orient/thumbnail/360x/strip/format/WEBP/quality/75!/ignore-error/1",
            "video_url": "https://video.picturehaven.net/video/" + data["play_url_privatization"],
            "platform": VideoPost.PLATFORM_TIKTOK,
            "content": clean_str(data["desc"]),
            "posted_at": datetime.fromtimestamp(data["create_time"]),
            "landing_page_url": data["root_path"] if "root_path" in data.keys() else "",
            "resolution": str(data["width"]) + "*" + str(data["height"]),
            "original_post_url": data["share_url"],
            "impression_count": data["play_count"],
            "like_count": data["interaction"],
            "comment_count": data["comment_count"],
            "share_count": data["share_count"],
            "crawler": VideoPost.CRAWLER_SHOPLUS
        }
        video_post = VideoPost.objects.create(**save_data)
        video_post.push_to_sheet()
        return video_post


class AccountCrawlerConfig(Preferences):
    henull_username = models.CharField("Tài khoản Henull", max_length=255, default="", blank=True)
    henull_password = models.CharField("Mật khẩu Henull", max_length=255, default="", blank=True)
    shoplus_username = models.CharField("Tài khoản Shoplus", max_length=255, default="", blank=True)
    shoplus_password = models.CharField("Mật khẩu Shoplus", max_length=255, default="", blank=True)

def image_path(instance, filename):
    import os
    return os.path.join('google_credential.json')

class SeleniumCrawlerConfig(Preferences):
    # headless = models.BooleanField("Chế độ cào không có giao diện", default=True)
    bigspy_running = models.BooleanField("Bigspy đang chạy", default=False)
    bigspy_crawled = models.PositiveIntegerField("Số lượng bài bigspy cào được", default=0)
    shoplus_running = models.BooleanField("Shoplus đang chạy", default=False)
    shoplus_crawled = models.PositiveIntegerField("Số lượng bài shoplus cào được", default=0)
    google_credential = models.FileField("Google Credential", max_length=255, storage=OverwriteStorage(), upload_to=image_path)
    