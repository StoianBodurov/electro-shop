from django.contrib import admin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@admin.register(UserModel)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    list_filter = ('is_staff', 'is_superuser')
    readonly_fields = ('date_joined',)
