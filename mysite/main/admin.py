from django.contrib import admin
from .models import WP, WPworld, WPseries

class WPAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/date", {'fields': ["wp_title", "wp_published"]}),
        ("URL", {'fields': ["wp_slug"]}),
        ("Series", {'fields': ["wp_series"]}),
        ("Content", {"fields": ["wp_content"]}),
		("Image", {"fields": ["wp_image"]})
    ]


admin.site.register(WPseries)
admin.site.register(WPworld)
admin.site.register(WP,WPAdmin)
