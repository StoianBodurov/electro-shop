import os
from os.path import join

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

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


class CreateItemView(CreateView):
    model = Item
    template_name = 'item/create item.html'
    success_url = reverse_lazy('home page')
    form_class = CreateItemForm


class EditItemView(UpdateView):
    model = Item
    form_class = EditItemForm
    template_name = 'item/edit item.html'

    def form_valid(self, form):
        db_item = Item.objects.get(id=self.kwargs['pk'])
        image_path = join(settings.MEDIA_ROOT, str(db_item.image))

        for field, value in form.cleaned_data.items():
            setattr(db_item, field, value)
            db_item.save()

        os.remove(image_path)
        return redirect('home page')


class DetailsItemView(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'item/details item.html'


class DeleteItemView(DeleteView):
    model = Item
    template_name = 'item/delete item.html'
    success_url = reverse_lazy('home page')
    context_object_name = 'item'

    def form_valid(self, form):
        success_url = self.get_success_url()
        db_item = Item.objects.get(id=self.kwargs['pk'])
        image_path = join(settings.MEDIA_ROOT, str(db_item.image))
        self.object.delete()
        os.remove(image_path)
        return redirect(success_url)
