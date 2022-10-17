from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'web_id',
            'slug',
            'name',
            'title',
            'content',
            'description',
            'public',
            'price',
            'is_active',
        ]
