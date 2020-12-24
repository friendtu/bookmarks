from django import forms
from .models import Image
from urllib import request
from django.utils.text import slugify
from django.core.files.base import ContentFile


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=["title","url","description"]
        widgets={
            'url':forms.HiddenInput,
        }

    def clean_url(self):
        url=self.cleaned_data['url']
        valid_extentions=['jpg','jpeg']
        extention=url.rsplit('.',1)[1].lower()
        if extention not in valid_extentions:
            raise forms.ValidationError('The given URL  doesn\'t not ' \
                    'match valid image extentions.')
        return url

    def save(self,commit=True):
        image=super().save(commit=False)
        image_url=self.cleaned_data['url']
        image_name='{}.{}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        response=request.urlopen(image_url)
        image.image.save(image_name,ContentFile(response.read()))
        if commit:
            image.save()
        return image





