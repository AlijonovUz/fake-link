from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Data


@admin.register(Data)
class DataAdmin(ModelAdmin):
    list_display = ('url', 'code', 'expire_days')
    list_display_links = ('url',)
    list_per_page = 10
    list_max_show_all = 100
