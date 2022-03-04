from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from users.forms import UserCreateForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
