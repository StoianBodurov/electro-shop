import os
from os.path import join

from django import forms
from django.conf import settings

from electroshop.store_app.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'categories': forms.Select(
                attrs={
                    'class': 'input',
                }
            ),
            'brand': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Brand'
                }
            ),
            'model': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Model'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'input',
                    'placeholder': 'Description'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Price'
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'input form-control',
                    'placeholder': 'Select Image',
                }
            ),
            'in_stock': forms.RadioSelect(
                choices=((True, 'In Stoke'), (False, 'Out of Stock')),
                attrs={
                    'class': 'radio-inline',
                }
            )
        }


class CreateItemForm(ItemForm):
    pass


class EditItemForm(ItemForm):
    pass


class DeleteItemForm(ItemForm):
    pass

