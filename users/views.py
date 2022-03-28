from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, FormView, ListView, TemplateView,
                                  UpdateView)

from events.models import Event
from users.forms import LoginForm, UserCreateForm, UserUpdateForm
from users.models import User


class UsersListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = ('admin',)
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('users:profile')


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    permission_required = ('admin',)
    extra_context = {
        'update_form': True,
        'cancel_url': reverse_lazy('users:all')
    }

    def get_success_url(self):
        return reverse_lazy('users:all')


class UserProfileView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'users/profile.html'
    queryset = Event.objects.all()
    context_object_name = 'events'


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated.'))
            return redirect('users:profile')

    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
        'update_form': True,
        'cancel_url': reverse_lazy('users:profile')
    }

    return render(request, 'users/user_form.html', context)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'users/logged_out.html'
