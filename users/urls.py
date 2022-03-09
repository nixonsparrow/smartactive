from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('new/', views.UserCreateView.as_view(), name='create-form'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update-form'),
]
