from crawler.models import VideoPost
videopost = VideoPost.objects.last()
videopost.title = "test"
videopost.save()