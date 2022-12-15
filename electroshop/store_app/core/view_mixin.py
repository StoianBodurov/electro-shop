from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin


class UserIsStaffMixin(PermissionRequiredMixin):
    permission_required = ('store_app.change_item', 'store_app.add_item')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_staff:
            logout(request)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)



