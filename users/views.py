from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserCreateForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('users:create-form')


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    permission_required = ('admin',)

    def get_success_url(self):
        return reverse_lazy('users:update-form', kwargs={'pk': self.get_object().id})
