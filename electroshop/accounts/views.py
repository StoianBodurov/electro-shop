from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from electroshop.accounts.forms import RegisterUserForm, LoginUserForm, EditProfileForm
from electroshop.accounts.models import Profile


class RegisterUserView(SuccessMessageMixin, CreateView):
    template_name = 'auth/register.html'
    success_url = reverse_lazy('home page')
    form_class = RegisterUserForm
    success_message = 'You are registered successfully'
    user = None

    def form_valid(self, form):
        response = super().form_valid(form)
        self.user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        login(self.request, self.user)
        return response


class LoginUserView(LoginView):
    template_name = 'auth/login.html'
    success_url = 'home'
    authentication_form = LoginUserForm


class LogoutUserView(LogoutView):
    pass


class UpdateUserProfile(UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'auth/profile.html'
    success_url = reverse_lazy('home page')
