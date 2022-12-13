from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.list import MultipleObjectMixin

from electroshop.common.forms import ReviewForm, FilterItemForm, SearchBarForm
from electroshop.common.models import Review
from electroshop.store_app.models import Item


class ItemReviewView(LoginRequiredMixin, MultipleObjectMixin, View):
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


class FilterListView(ListView):
    model = Item
    form_class = FilterItemForm
    template_name = 'store/store.html'
    paginate_by = 6
    context_object_name = 'items'

    def get_queryset(self):
        categories = self.request.GET.get('categories')
        price_min = float(self.request.GET.get('price_min'))
        price_max = float(self.request.GET.get('price_max'))
        brand = self.request.GET.get('brand') if self.request.GET.get('brand') else 'other'

        if not categories:
            if brand == 'other':
                return Item.objects.filter(price__gt=price_min, price__lte=price_max)
            return Item.objects.filter(price__gt=price_min, price__lte=price_max, brand__icontains=brand)
        else:
            if brand == 'other':
                return Item.objects.filter(categories__icontains=categories, price__gt=price_min, price__lte=price_max)
            return Item.objects.filter(categories__icontains=categories, price__gt=price_min, price__lte=price_max,
                                       brand__icontains=brand)


class SearchListView(ListView):
    model = Item
    form_class = SearchBarForm
    template_name = 'store/store.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self):
        search_text = self.request.GET.get('search_text')
        categories = self.request.GET.get('categories')

        if categories == 'all':
            return Item.objects.filter(Q(categories__icontains=search_text) | Q(model__icontains=search_text) |
                                       Q(brand__icontains=search_text))

        return Item.objects.filter(
            Q(categories__iexact=categories) & (Q(model__icontains=search_text) | Q(brand__icontains=search_text)))
