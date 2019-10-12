import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from bell.models import Bell, Event


def index_view(request):
    """Представление главной страницы"""

    return render(request, 'index.html')


def new_bell(request):
    """создание колокольчика"""
    title = request.POST.get("bell_title")
    bell = Bell.objects.create(title=title)

    return redirect('bell_view', bell.link_ref)


def bell_view(request, link_ref):
    """представление колокольчика"""
    bell = Bell.objects.get(link_ref=link_ref)
    return render(request, 'bell.html', context={"bell": bell})


def last_event(request, link_ref):
    """получить последнее событие колокольчика"""

    event = Event.objects.filter(bell__link_ref=link_ref).last()
    if event:
        return JsonResponse({"text": event.text, "read": event.read})
    return JsonResponse({})


@csrf_exempt
def latest_events(request, link_ref):
    """получить последние события колокольчика"""
    bell = Bell.objects.get(link_ref=link_ref)
    events_dict = list(Event.objects.latest(bell).values("text", "read"))
    return JsonResponse(events_dict, safe=False)


@csrf_exempt
def read_events(request, link_ref):
    """отметить прочитанным все события колокольчика"""
    Event.objects.filter(bell__link_ref=link_ref).update(read=True)
    Event.objects.update(read=True)
    return redirect('last_event', link_ref)


@csrf_exempt
def new_event(request, link_ref):
    """добавление нового события"""
    bell = Bell.objects.get(link_ref=link_ref)
    text = request.POST.get("text")
    event = Event.objects.create(bell=bell, text=text)
    return JsonResponse({"status": "ok"})
