from django.contrib import admin
from django.contrib.admin import register

# Register your models here.
from links.models import Link, Collection


@register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "url", "type", "created_at", "owners"]
    list_display_links = ["pk", "url"]
    list_filter = ["type", "owners", "collections"]
    list_per_page = 15


@register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "created_at", "owners"]
    list_display_links = ["pk", "title"]
    list_filter = ["owners"]
    list_per_page = 15
