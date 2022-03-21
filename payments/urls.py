from django.urls import path

from payments import views

app_name = 'payments'

urlpatterns = [
    path('', views.Overview.as_view(), name='overview'),
]
