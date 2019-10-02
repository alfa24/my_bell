from django.urls import path
from .views import new_bell, bell_view, new_event

urlpatterns = [
    path('new', new_bell, name='new_bell'),
    path('<link_ref>/events/add', new_event, name='new_event'),
    path('<link_ref>/', bell_view, name='bell_view')
]
