from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('', views.UsersListView.as_view(), name='all'),
    path('new/', views.UserCreateView.as_view(), name='create-form'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update-form'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
]
