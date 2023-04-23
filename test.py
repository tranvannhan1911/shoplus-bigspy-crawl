from crawler.models import VideoPost
videopost = VideoPost.objects.last()
videopost.push_to_sheet()