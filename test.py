from crawler.models import VideoPost

vd = VideoPost.objects.filter(crawler="shoplus").first()
print(vd.ads_id)
vd.save()
vd = VideoPost.objects.first()
vd.save()