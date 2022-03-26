from django.urls import path

from events import views

app_name = 'calendar'

urlpatterns = [
    path('', views.Overview.as_view(), name='overview'),
    path('<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
]
