from django import forms
from .models import GemstoneImage

class GemstoneImageForm(forms.ModelForm):
    class Meta:
        model = GemstoneImage
        fields = ['image']
