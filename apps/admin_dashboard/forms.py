from django import forms
from apps.store.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "description", "price", "stock", "category", "images", "is_availbale"]


        
        widgets = {
            "product_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Wooden Chair",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Short description of the product",
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),
            "stock": forms.NumberInput(attrs={
                "class": "form-control",
            }),
            "category": forms.Select(attrs={
                "class": "form-control",
            }),
            "images": forms.ClearableFileInput(attrs={
                "class": "form-control-file",
            }),
            "is_availbale": forms.CheckboxInput(attrs={
                "class": "form-checkbox-input",
            }),
        }