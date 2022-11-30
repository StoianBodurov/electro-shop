from django.urls import path

from electroshop.common.views import ItemReviewView, FilterListView, SearchListView

urlpatterns = (
    path('review/<int:pk>', ItemReviewView.as_view(), name='review item'),
    path('filter/', FilterListView.as_view(), name='filter result'),
    path('search/', SearchListView.as_view(), name='search result'),
)
