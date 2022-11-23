from django.urls import path

from electroshop.accounts.views import RegisterUserView, LoginUserView, LogoutUserView, UpdateUserProfile

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='user register'),
    path('login/', LoginUserView.as_view(), name='user login'),
    path('logout/', LogoutUserView.as_view(), name='user logout'),
    path('profile/<int:pk>', UpdateUserProfile.as_view(), name='user profile'),
)