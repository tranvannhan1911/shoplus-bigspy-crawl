# Generated by Django 3.2.18 on 2023-04-23 15:56

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django_countries.fields
import gsheets.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('preferences', '0003_alter_preferences_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountCrawlerConfig',
            fields=[
                ('preferences_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='preferences.preferences')),
                ('henull_username', models.CharField(blank=True, default='', max_length=255, verbose_name='Tài khoản Henull')),
                ('henull_password', models.CharField(blank=True, default='', max_length=255, verbose_name='Mật khẩu Henull')),
                ('shoplus_username', models.CharField(blank=True, default='', max_length=255, verbose_name='Tài khoản Shoplus')),
                ('shoplus_password', models.CharField(blank=True, default='', max_length=255, verbose_name='Mật khẩu Shoplus')),
            ],
            bases=('preferences.preferences',),
            managers=[
                ('singleton', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SeleniumCrawlerConfig',
            fields=[
                ('preferences_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='preferences.preferences')),
                ('bigspy_running', models.BooleanField(default=False, verbose_name='Bigspy đang chạy')),
                ('bigspy_crawled', models.PositiveIntegerField(default=0, verbose_name='Số lượng bài bigspy cào được')),
                ('shoplus_running', models.BooleanField(default=False, verbose_name='Shoplus đang chạy')),
                ('shoplus_crawled', models.PositiveIntegerField(default=0, verbose_name='Số lượng bài shoplus cào được')),
            ],
            bases=('preferences.preferences',),
            managers=[
                ('singleton', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='VideoPost',
            fields=[
                ('guid', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False)),
                ('ads_id', models.CharField(max_length=255, verbose_name='Ads id')),
                ('title', models.CharField(blank=True, default='', max_length=255, verbose_name='Tiêu đề')),
                ('fanpage_name', models.CharField(blank=True, default='', max_length=255, verbose_name='Tên fanpage')),
                ('fanpage_url', models.CharField(blank=True, default='', max_length=255, verbose_name='Link fanpage')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Quốc gia')),
                ('content', models.TextField(blank=True, default='', verbose_name='Nội dung')),
                ('thumbnail_url', models.CharField(blank=True, default='', max_length=255, verbose_name='Thumbnail')),
                ('avatar', models.CharField(blank=True, default='', max_length=255, verbose_name='Avatar')),
                ('video_url', models.CharField(blank=True, default='', max_length=255, verbose_name='Video URL')),
                ('platform', models.CharField(choices=[('facebook', 'facebook'), ('tiktok', 'tiktok')], max_length=255, verbose_name='Nền tảng')),
                ('landing_page_url', models.CharField(blank=True, default='', max_length=255, verbose_name='Landing Page URL')),
                ('resolution', models.CharField(blank=True, default='', max_length=255, verbose_name='Độ phân giải')),
                ('original_post_url', models.CharField(blank=True, default='', max_length=255, verbose_name='Bài viết gốc')),
                ('impression_count', models.IntegerField(default=0, verbose_name='Impression')),
                ('like_count', models.IntegerField(default=0, verbose_name='Lượt like')),
                ('comment_count', models.IntegerField(default=0, verbose_name='Lượt bình luận')),
                ('share_count', models.IntegerField(default=0, verbose_name='Lượt share')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày thu thập')),
                ('posted_at', models.DateTimeField(verbose_name='Ngày đăng')),
                ('crawler', models.CharField(choices=[('bigspy', 'bigspy'), ('shoplus', 'shoplus')], max_length=255, verbose_name='Nền tảng cào')),
            ],
            bases=(gsheets.mixins.SheetPushableMixin, models.Model),
        ),
    ]