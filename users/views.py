from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserCreateForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('user-create-form')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy('user-update-form', kwargs={'pk': self.get_object().id})
