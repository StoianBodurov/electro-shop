from django import forms

from electroshop.common.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review', 'rating')
        widgets = {
            'review': forms.Textarea(
                attrs={
                    'class': 'input',
                    'placeholder': 'Your Review'
                }
            ),
            'rating': forms.RadioSelect(choices=(
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
                (5, 5)
            ))
        }


class FilterItemForm(forms.Form):
    categories = forms.CheckboxInput()
    price_min = forms.NumberInput()
    price_max = forms.NumberInput()
    brand = forms.CheckboxInput()


class SearchBarForm(forms.Form):
    categories = forms.ChoiceField(choices=(
        ('all', 'all'),
        ('laptops', 'laptops'),
        ('smartphones', 'smartphones'),
        ('cameras', 'cameras'),
        ('accessories', 'accessories'),
    ))
    search_text = forms.TextInput()
