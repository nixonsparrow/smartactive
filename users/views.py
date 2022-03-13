from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView, LogoutView
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from events.models import Event
from users.forms import LoginForm, UserCreateForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('users:profile')


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    permission_required = ('admin',)

    def get_success_url(self):
        return reverse_lazy('users:update-form', kwargs={'pk': self.get_object().id})


class UserProfileView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'users/profile.html'
    queryset = Event.objects.all()
    context_object_name = 'events'


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'users/logged_out.html'
