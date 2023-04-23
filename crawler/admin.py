from django.contrib import admin
from .models import VideoPost, AccountCrawlerConfig, SeleniumCrawlerConfig
from rangefilter.filters import DateRangeFilterBuilder
from import_export.admin import ExportActionMixin
from django.contrib.admin.filters import AllValuesFieldListFilter
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter
)
from django.utils.translation import gettext_lazy as _
from django_countries.data import COUNTRIES
from preferences.admin import PreferencesAdmin

class MyDropdownFilter(DropdownFilter):
    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None and self.lookup_val_isnull is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        include_none = False
        for val in self.lookup_choices:
            if val is None:
                include_none = True
                continue
            val = str(val)
            display = COUNTRIES[val]
            yield {
                'selected': self.lookup_val == val,
                'query_string': changelist.get_query_string({self.lookup_kwarg: val}, [self.lookup_kwarg_isnull]),
                'display': display,
            }
        if include_none:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }

class VideoPostAdmin(ExportActionMixin, admin.ModelAdmin):
    exclude = ["ads_id", "created_at"]
    # fields = [field.name for field in VideoPost._meta.get_fields() if field.name != "created_at" and field.name != "ads_id"]
    list_display = [field.name for field in VideoPost._meta.get_fields()]
    ordering = ["-created_at"]
    search_fields = ('ads_id', 'title', 'fanpage_name', 'country', 'platform', 'content')
    list_filter =('crawler', 'platform', 
                  ('created_at', DateRangeFilterBuilder()), 
                  ('posted_at', DateRangeFilterBuilder()),
                #   ('country', MyDropdownFilter),
                  ('resolution', DropdownFilter))
    list_per_page = 200
    change_list_template = "admin/videopost/change_list.html"
    
admin.site.register(VideoPost, VideoPostAdmin)
admin.site.register(AccountCrawlerConfig, PreferencesAdmin)
admin.site.register(SeleniumCrawlerConfig, PreferencesAdmin)