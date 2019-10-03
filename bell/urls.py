from django.urls import path
from .views import new_bell, bell_view, new_event, last_event, read_events, latest_events

urlpatterns = [
    path('new', new_bell, name='new_bell'),
    path('<link_ref>/events/add', new_event, name='new_event'),
    path('<link_ref>/events/read', read_events, name='read_events'),
    path('<link_ref>/events/last/', last_event, name='last_event'),
    path('<link_ref>/events/latest/', latest_events, name='latest_events'),
    path('<link_ref>/', bell_view, name='bell_view')
]
