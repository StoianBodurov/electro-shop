import os
from os.path import join

from django import forms
from django.conf import settings

from electroshop.store_app.models import Item, Order


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
                    'class': 'custom-file-upload',
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
    # def save(self, commit=True):
    #     db_item = Item.objects.get(pk=self.instance.id)
    #     if commit:
    #         image_path = join(settings.MEDIA_ROOT, str(db_item.image))
    #         try:
    #             os.remove(image_path)
    #         except:
    #             pass
    #
    #     return super().save(commit)

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
                    'class': 'custom-file-input',
                }
            ),
            'in_stock': forms.RadioSelect(
                choices=((True, 'In Stoke'), (False, 'Out of Stock')),
                attrs={
                    'class': 'radio-inline',
                }
            ),
        }


class DeleteItemForm(ItemForm):
    pass


class OrderForm(forms.Form):
    quantity = forms.IntegerField()

    class Meta:
        model = Order
        fields = ('quantity',)
