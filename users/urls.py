from django.urls import path
from users import views


urlpatterns = [
    path('new/', views.UserCreateView.as_view(), name='user-create-form'),
    path('profile/<int:pk>', views.UserUpdateView.as_view(), name='user-update-form'),
]
