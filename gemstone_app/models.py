from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class GemstoneImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gemstones/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ColorAnalysis(models.Model):
    gemstone_image = models.ForeignKey('GemstoneImage', on_delete=models.CASCADE)
    rgb = models.CharField(max_length=20) 
    css_color_code = models.CharField(max_length=7)
    brightness = models.FloatField()
    color_ratios = models.CharField(max_length=50)
    density = models.FloatField()
    closest_colors = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Color Analysis ({self.rgb}) - {self.closest_colors}"



