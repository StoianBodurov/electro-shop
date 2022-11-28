from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import MultipleObjectMixin

from electroshop.common.forms import ReviewForm
from electroshop.common.models import Review
from electroshop.store_app.models import Item


class ItemReviewView(MultipleObjectMixin, View):
    form_class = ReviewForm
    context_object_name = 'reviews'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        item = Item.objects.get(pk=self.kwargs['pk'])
        rating = form.cleaned_data['rating']
        if not rating:
            rating = 0

        review = Review(
            review=form.cleaned_data['review'],
            rating=rating,
            item=item,
            user=self.request.user
        )
        review.save()
        return redirect('details item', item.id)
