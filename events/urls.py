from django.urls import path

from events import views

app_name = 'calendar'

urlpatterns = [
    path('', views.Overview.as_view(), name='overview'),
    path('<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('events/', views.EventListView.as_view(), name='events-all'),
    path('events/new/', views.EventCreateView.as_view(), name='events-new'),
    path('events/update/<int:pk>/', views.EventUpdateView.as_view(), name='events-update'),
    path('tickets/', views.TicketListView.as_view(), name='tickets-all'),
    path('tickets/new/', views.TicketCreateView.as_view(), name='tickets-new'),
    path('tickets/update/<int:pk>/', views.TicketUpdateView.as_view(), name='tickets-update'),
]
