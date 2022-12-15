from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

from electroshop.common.forms import ReviewForm
from electroshop.common.models import Review
from electroshop.store_app.core.view_mixin import UserIsStaffMixin
from electroshop.store_app.forms import CreateItemForm, EditItemForm, OrderForm
from electroshop.store_app.models import Item, Order
from electroshop.store_app.utils.helpers import get_order_total_price


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


class CreateItemView(UserIsStaffMixin, CreateView):
    model = Item
    template_name = 'item/create item.html'
    success_url = reverse_lazy('home page')
    form_class = CreateItemForm
    categories_name = 'create_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_name'] = self.categories_name
        return context


class EditItemView(UserIsStaffMixin, UpdateView):
    model = Item
    form_class = EditItemForm
    template_name = 'item/edit item.html'
    success_url = reverse_lazy('home page')


class DetailsItemView(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'item/details item.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context['item']
        reviews = Review.objects.filter(item_id=item.id).order_by('date_added')

        paginator = Paginator(reviews, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        average_rating = reviews.aggregate(Avg('rating'))
        context['page_obj'] = page_obj
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


class DeleteItemView(UserIsStaffMixin, DeleteView):
    model = Item
    template_name = 'item/delete item.html'
    success_url = reverse_lazy('home page')
    context_object_name = 'item'


class AddItemToOrderView(LoginRequiredMixin, View):
    model = Order
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        user = self.request.user
        item = Item.objects.get(pk=self.kwargs['pk'])
        order = Order(
            quantity=form.cleaned_data['quantity'],
            item=item,
            user=user
        )
        order.save()
        return redirect('details item', item.id)


class OrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(user_id=user.id, status='added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']
        total_price = get_order_total_price(orders)
        context['total_price'] = total_price

        return context


class OrderRemove(LoginRequiredMixin, View):
    model = Order

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        order.status = 'canceled'
        order.save()
        return redirect('orders list')
