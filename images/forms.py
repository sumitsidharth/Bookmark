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
    image_file = forms.ImageField(required=False, label="Upload Image File")

    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput(),
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        image_file = self.cleaned_data.get('image_file')

        if not url and not image_file:
            raise forms.ValidationError("Either a URL or an image file is required.")

        if url:
            valid_extensions = ['jpg', 'jpeg', 'png']
            try:
                extension = url.split('.')[-1].split('?')[0].lower()
                if extension not in valid_extensions:
                    raise forms.ValidationError(
                        "The given URL does not match a valid image extension."
                    )
            except Exception:
                raise forms.ValidationError("Invalid URL format.")

        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data.get('url')
        image_file = self.cleaned_data.get('image_file')

        # Prioritize manual upload
        if image_file:
            image.image.save(image_file.name, image_file, save=False)
            # If no URL was provided, set a placeholder or use the name
            if not image_url:
                image.url = f"uploaded://{image_file.name}"
        elif image_url:
            name = slugify(image.title)
            extension = image_url.split('.')[-1].split('?')[0].lower()
            if extension not in ['jpg', 'jpeg', 'png']:
                extension = 'jpg'
            image_name = f"{name}.{extension}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
            try:
                response = requests.get(image_url, headers=headers, timeout=10)
                if response.status_code != 200:
                    raise ValueError(f"Server returned status {response.status_code}")
                
                image.image.save(
                    image_name,
                    ContentFile(response.content),
                    save=False
                )
            except requests.exceptions.ProxyError:
                raise ValueError(
                    "The server is blocked by a proxy. This is common on PythonAnywhere Free accounts. "
                    "Please download the image and upload it using the 'Upload Image File' field instead."
                )
            except requests.exceptions.RequestException as e:
                raise ValueError(f"Failed to download image: {str(e)}")
        else:
            raise ValueError("No image source provided.")

        if commit:
            image.save()

        return image