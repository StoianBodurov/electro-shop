from django.urls import path

from electroshop.store_app.views import LastAddedItemView, CreateItemView, EditItemView, DetailsItemView, \
    DeleteItemView, ListItemByCategoriesView, AddItemToOrderView, OrdersListView, OrderRemove

urlpatterns = (
    path('', LastAddedItemView.as_view(), name='home page'),
    path('create/', CreateItemView.as_view(), name='create item'),
    path('edit/<int:pk>', EditItemView.as_view(), name='edit item'),
    path('details/<int:pk>', DetailsItemView.as_view(), name='details item'),
    path('delete/<int:pk>', DeleteItemView.as_view(), name='delete item'),
    path('store/<str:categories>', ListItemByCategoriesView.as_view(), name='store page'),
    path('addorder/<int:pk>', AddItemToOrderView.as_view(), name='add order'),
    path('orders_list/', OrdersListView.as_view(), name='orders list'),
    path('order_remove/<int:pk>', OrderRemove.as_view(), name='orders remove'),
)
