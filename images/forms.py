# pyrefly: ignore [missing-import]
from django import forms
# pyrefly: ignore [missing-import]
from .models import Image
import requests
# pyrefly: ignore [missing-import]
from django.core.files.base import ContentFile
# pyrefly: ignore [missing-import]
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput(),
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')

        if not url:
            raise forms.ValidationError("URL is required.")

        valid_extensions = ['jpg', 'jpeg', 'png']

        try:
            extension = url.split('.')[-1].split('?')[0].lower()
        except Exception:
            raise forms.ValidationError("Invalid URL format.")

        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not match a valid image extension."
            )

        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data.get('url')

        if not image_url:
            raise ValueError("No URL provided")

        name = slugify(image.title)

        # safer extension extraction
        extension = image_url.split('.')[-1].split('?')[0].lower()
        if extension not in ['jpg', 'jpeg', 'png']:
            extension = 'jpg'

        image_name = f"{name}.{extension}"

        # download image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise ValueError("Failed to download image")

        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False
        )

        if commit:
            image.save()

        return image