from django.urls import path

from electroshop.common.views import ItemReviewView, FilterListView

urlpatterns = (
    path('review/<int:pk>', ItemReviewView.as_view(), name='review item'),
    path('filter/', FilterListView.as_view(), name='filter result'),
)
