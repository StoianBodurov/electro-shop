from django.db.models import Avg
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

from electroshop.common.forms import ReviewForm
from electroshop.common.models import Review
from electroshop.store_app.forms import CreateItemForm, EditItemForm
from electroshop.store_app.models import Item


class LastAddedItemView(ListView):
    model = Item
    template_name = 'home page/home.html'
    context_object_name = 'items'
    categories_name = 'home'

    def get_queryset(self):
        return Item.objects.all().order_by('-date_added')[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_name'] = self.categories_name
        return context


class ListItemByCategoriesView(ListView):
    model = Item
    template_name = 'store/store.html'
    context_object_name = 'items'
    paginate_by = 6
    categories_name = ''

    def get_queryset(self):
        self.categories_name = self.kwargs['categories']
        if self.categories_name == 'all':
            return Item.objects.order_by('-date_added')
        return Item.objects.filter(categories=self.categories_name).order_by('-date_added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_name'] = self.categories_name
        return context


class CreateItemView(CreateView):
    model = Item
    template_name = 'item/create item.html'
    success_url = reverse_lazy('home page')
    form_class = CreateItemForm
    categories_name = 'create_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_name'] = self.categories_name
        return context


class EditItemView(UpdateView):
    model = Item
    form_class = EditItemForm
    template_name = 'item/edit item.html'
    success_url = reverse_lazy('home page')


class DetailsItemView(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'item/details item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context['item']
        reviews = Review.objects.filter(item_id=item.id).order_by('date_added')

        average_rating = reviews.aggregate(Avg('rating'))
        context['reviews'] = reviews
        context['average_rating'] = 0
        if average_rating['rating__avg']:
            context['average_rating'] = round(average_rating['rating__avg'], 1)

        context['review_form'] = ReviewForm(
            initial={
                'item_id': self.object.id
            }
        )
        return context


class DeleteItemView(DeleteView):
    model = Item
    template_name = 'item/delete item.html'
    success_url = reverse_lazy('home page')
    context_object_name = 'item'
