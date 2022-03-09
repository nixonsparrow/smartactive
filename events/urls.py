from django.urls import path

from events import views

app_name = 'events'

urlpatterns = [
    path('', views.Overview.as_view(), name='overview'),
]
