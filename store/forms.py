from django import forms

from store.models import Product


class ProductForms(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'digital',
            'image',
            'width_field',
            'height_field',
            'content',
        ]
