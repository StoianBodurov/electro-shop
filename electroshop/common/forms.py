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
