from django.contrib import admin

from electroshop.store_app.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('categories', 'brand', 'model', 'description', 'price', 'image', 'in_stock', 'date_added')
    list_filter = ('categories', 'brand', 'model', 'description', 'price', 'image', 'in_stock', 'date_added')
    fieldsets = ((None, {
        'fields': ('categories', 'brand', 'model', 'description', 'price', 'image', 'in_stock')
    }),)
