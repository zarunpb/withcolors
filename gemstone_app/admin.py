from django.contrib import admin

# Register your models here.
from .models import ColorAnalysis

@admin.register(ColorAnalysis)
class ColorAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'gemstone_image', 'rgb', 'css_color_code', 'brightness', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('rgb', 'css_color_code', 'closest_colors')

    def closest_colors_display(self, obj):
        return ", ".join([f"{color['name']} ({color['percentage']}%)" for color in obj.closest_colors])

    closest_colors_display.short_description = "Top 3 Colors"
