from django.urls import path

from payments import views

app_name = 'payments'

urlpatterns = [
    path('', views.Overview.as_view(), name='all'),
    path('new/', views.PaymentCreateView.as_view(), name='new'),
    path('update/<int:pk>/', views.PaymentUpdateView.as_view(), name='update'),
]
