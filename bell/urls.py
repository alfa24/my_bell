from django.urls import path
from .views import new_bell, bell_view

urlpatterns = [
    path('new', new_bell, name='new_bell'),
    path('<code>/', bell_view, name='bell_view')
]
