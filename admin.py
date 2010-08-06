from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from pages.models import Page


PAGE_INLINES = []

if 'media' in settings.INSTALLED_APPS:
    try:
        from media.models import MediaSet
    except:
        pass
    else:
        class PageMediaInline(GenericTabularInline):
            extra = 1
            max_num = 1
            model = MediaSet
        
        PAGE_INLINES += [PageMediaInline]


if 'ctas' in settings.INSTALLED_APPS:
    try:
        from ctas.models import AttachedCallToAction
    except:
        pass
    else:
        class PageCallToActionInline(GenericTabularInline):
            extra = 1
            max_num = 1
            model = AttachedCallToAction
        
        PAGE_INLINES += [PageCallToActionInline]


class PageAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish_at'
    inlines = PAGE_INLINES
    list_display = ['title', 'url', 'publish_at', 'is_enabled']
    #list_filter = ['is_enabled']
    prepopulated_fields = {'url': ['title']}
    search_fields = ['title', 'headline', 'url']
    
    def save_model(self, request, obj, form, change):
        if not change: obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

admin.site.register(Page, PageAdmin)