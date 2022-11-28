from django.urls import path

from electroshop.common.views import ItemReviewView

urlpatterns = (
    path('review/<int:pk>', ItemReviewView.as_view(), name='review item'),
)
