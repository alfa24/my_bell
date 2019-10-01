from django.shortcuts import render, redirect


# Create your views here.
from bell.models import Bell


def index_view(request):
    """Представление главной страницы"""

    return render(request, 'index.html')


def new_bell(request):
    """создание колокольчика"""
    bell = Bell.objects.create()

    return redirect('bell_view', bell.link_ref)


def bell_view(request, code):
    """представление колокольчика"""

    return render(request, 'bell.html')
