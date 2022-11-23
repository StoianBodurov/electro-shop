from django.urls import path

from electroshop.store_app.views import home

urlpatterns = (
    path('', home, name='home'),
)