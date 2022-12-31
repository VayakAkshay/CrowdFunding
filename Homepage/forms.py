from django import forms
from .models import Blog_data

class ImageForm(forms.ModelForm):
    class Meta:
        model = Blog_data
        fields = ["blog_img"]
        labels = {"blog_img": ""}