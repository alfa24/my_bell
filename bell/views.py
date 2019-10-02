from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

from bell.models import Bell, Event


def index_view(request):
    """Представление главной страницы"""

    return render(request, 'index.html')


def new_bell(request):
    """создание колокольчика"""
    bell = Bell.objects.create()

    return redirect('bell_view', bell.link_ref)


def bell_view(request, link_ref):
    """представление колокольчика"""
    bell = Bell.objects.get(link_ref=link_ref)
    return render(request, 'bell.html', context={"bell": bell})


def new_event(request, link_ref):
    """добавление нового события"""
    bell = Bell.objects.get(link_ref=link_ref)
    text = request.POST.get("text")
    event = Event.objects.create(bell=bell, text=text)
    return HttpResponse({"status": "ok"})